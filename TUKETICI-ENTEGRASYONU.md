# Tüketici Entegrasyon Kılavuzu

Bu depoyu kullanan projelerin (Sitematik, enakillitercih ve sonrakiler) izlemesi
gereken yol. Sitematik'te uygulanmış ve üretimde çalışan desendir.

---

## 1. Adresler

```
CDN (birincil) : https://cdn.jsdelivr.net/gh/hasakguldev/acik-veri@main
Raw (yedek)    : https://raw.githubusercontent.com/hasakguldev/acik-veri/main
```

Alan adı hiçbir yerde sabit yazılmaz; tek bir yapılandırma değişkeninden okunur
(`VITE_DATA_URL`, `site.config.json` vb.) ve varsayılanı yukarıdaki CDN'dir.

---

## 2. Hangi dosyayı ne zaman çekmeli

| İhtiyaç | Dosya | Boyut |
|---|---|---|
| Tercih listesi, filtreleme, sıralama | `yks/light/<tur>.json` | 80 KB – 1,12 MB |
| Tek programın tüm geçmişi, detay ekranı | `yks/programs_<tur>.json` | 0,55 – 7,65 MB |
| Lise tercih listesi | `lgs/light/schools.json` | 337 KB |
| Yetenek sınavı okulları | `lgs/light/yetenek.json` | 35 KB |
| Vergi / SGK / harç parametreleri | `parametreler/<yil>.json` | 2,3 KB |
| Katalog, sürüm, hangi veri var | `manifest.json` | 2 KB |

> **Kural:** Liste ve filtreleme için **daima hafif indeksi** kullanın. Tam
> dosyalar yalnızca tek bir programın ayrıntısı gerektiğinde, tembel olarak
> çekilmelidir.

---

## 3. Hafif indeks biçimi

Sözlük kodlamalı; tekrar eden metinler bir kez yazılır, satırlar dizidir.
Tam veriden **%75-90 küçüktür**.

```json
{
  "scoreType": "SAY",
  "year": 2026,
  "count": 5757,
  "dicts": {
    "univ":    ["ABDULLAH GÜL ÜNİVERSİTESİ", "…"],
    "city":    ["KAYSERİ", "…"],
    "program": ["Bilgisayar Mühendisliği", "…"],
    "faculty": ["MÜHENDİSLİK FAKÜLTESİ", "…"]
  },
  "fields": ["code","u","c","p","f","sch","lang","edu","type",
             "minScore","minRank","quota","prevScore","prevRank",
             "scoreYear","prevScoreYear","rankYear","prevRankYear",
             "proj","trend"],
  "rows": [
    ["106510077", 0, 0, 0, 0, "none", "en", "formal", 0,
     443.23, 46890, 80, 442.53, 40125, 2026, 2025, 2024, 2022, 46890, "flat"]
  ]
}
```

`u`, `c`, `p`, `f` sütunları `dicts` içindeki **indekstir** (`-1` = null).
`type`: `0` DEVLET, `1` VAKIF, `2` KKTC **veya yurt dışı** — ayrımı şehir
adından yapın (`KKTC-` ile başlıyorsa KKTC).

### Yıl sütunları — uydurmayın, okuyun

ÖSYM taban puanı ile başarı sırasını aynı takvimde yayımlamaz. Bu yüzden bir
satırın puanı ile sırası **farklı yıllara** ait olabilir:

| Sütun | Anlamı |
|---|---|
| `scoreYear` | `minScore` / `quota` hangi yıla ait |
| `prevScoreYear` | `prevScore` hangi yıla ait |
| `rankYear` | `minRank` hangi yıla ait |
| `prevRankYear` | `prevRank` hangi yıla ait |
| `proj` | çok yıllı trendden üretilmiş öngörülen sıra |
| `trend` | `"up"` (zorlaşıyor) / `"down"` (kolaylaşıyor) / `"flat"` |

Arayüzde yıl etiketini **daima bu sütunlardan** basın. `year` alanı yalnızca
indeksin genel yılıdır; satır bazında `scoreYear` bağlayıcıdır.

LGS indeksi aynı mantıkta: `dicts.{city,district,school,type,field}` ve
`fields: ["code","c","d","s","t","f","cat","minScore","quota","lang","boarding"]`.

### Çözme deseni

Filtrelemeyi **ham satırlar üzerinde** yapın; nesneye dönüşümü yalnızca ekrana
gelecek satırlar için uygulayın. 10.000 satırlık indeks böylece anında
filtrelenir. Sitematik'teki hazır uygulama:
`public/js/core/light-index.js` (`HafifIndeks` sınıfı, `filtrele()` metodu).

---

## 4. Dayanıklılık zinciri

İstemci şu sırayı izlemelidir:

1. **Bellek önbelleği** — aynı oturumda tekrar indirme yok
2. **localStorage** — ziyaretler arası (24 saat TTL, kayıt başına 2 MB üst sınır)
3. **jsDelivr CDN** — birincil
4. **GitHub Raw** — CDN erişilemezse
5. **Yerel varsayılan** — parametreler için son çare

Ek olarak: aynı dosyaya eşzamanlı istekler **tekilleştirilmeli** (uçuş hâlindeki
promise paylaşılır), kota dolduğunda önbellek kendini temizlemelidir.

Hazır uygulama: `public/js/core/acikVeri.js` (Sitematik).

---

## 5. Bilinen tuzaklar

| Tuzak | Belirti | Çözüm |
|---|---|---|
| `Infinity` JSON'da yok | Vergi dilimlerinin son basamağı `"limit": null` | Bilinen üst-sınır alanlarında `null` → `Infinity` çevirisi yapın |
| Anahtar adı farkı | `sgk.isciPayi` (uzak) ≠ `sgk.iscipayi` (yerel) | Normalizasyon katmanında eşleme haritası tutun |
| Uzak parametreler alt küme | 26 anahtar var, tüketicide ~70 | Uzak veri yereli **değiştirmez, üzerine yazar**; eksik anahtarlar korunur |
| Şehir alanı boş olabilir | Bazı programlarda `city` null | Arayüzde `—` gösterin, filtrede boşları dışlayın |
| Puan yılı ≠ sıra yılı | 2026 taban puanının yanında 2024 sırası | `scoreYear` / `rankYear` sütunlarını okuyun; ikisini tek yıl gibi göstermeyin |
| Yurt dışı programlar KKTC kovasında | `type: 2` hem KKTC hem yurt dışı | Şehir `KKTC-` ile başlıyorsa KKTC, değilse yurt dışı |

---

## 6. Veri güncelleme akışı

```bash
python scripts/convert_yks.py          # ham veri → tam JSON
python scripts/build_light_index.py    # tam JSON → hafif indeks
python scripts/verify_repo.py          # tutarlılık denetimi
git commit -am "veri: 2027 yerleştirme sonuçları" && git push
```

jsDelivr birkaç dakikada dağıtır. **Tüketici projelerde kod değişikliği
gerekmez**; istemcinin 24 saatlik önbelleği dolduğunda yeni veri gelir.

Acil yayılma gerekiyorsa jsDelivr önbelleği elle temizlenebilir:
`https://purge.jsdelivr.net/gh/hasakguldev/acik-veri@main/<dosya>`

---

## 7. Referans uygulama

Sitematik'teki çalışan kod, kopyalanabilir hâlde:

| Dosya | İşlev |
|---|---|
| `public/js/core/acikVeri.js` | CDN istemcisi, önbellek, yedek zinciri |
| `public/js/core/light-index.js` | Sözlük kodlamalı indeks çözücü ve filtreleyici |
| `public/js/core/remote-params.js` | Parametre normalizasyonu ve üzerine yazma |

Depo: `C:\Users\HP\proje\planlanan\sitematik\sitem`
