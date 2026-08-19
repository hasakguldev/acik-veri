# acik-veri

Türkiye eğitim, sınav, finans ve mevzuat verilerini içeren **merkezi açık veri deposu**.

Bu repo, birden fazla projenin (Sitematik, enakillitercih, vb.) ortak veri kaynağı olarak kullanılması için tasarlanmıştır. Veriler **jsDelivr CDN** üzerinden ücretsiz ve hızlı şekilde dağıtılır.

## Veri Setleri

### YKS Üniversite Yerleştirme Verileri (`yks/`)

ÖSYM YKS merkezi yerleştirme taban/tavan puanları, kontenjanlar ve bölüm istatistikleri.

| Yıl | Toplam Program | Dosya |
|-----|---------------|-------|
| 2026 | ~20.700+ | `yks/2026/*.json` |
| 2025 | ~20.800+ | `yks/2025/*.json` |

**Dosyalar:**
- `programs_tyt.json` — TYT (ön lisans) programları
- `programs_say.json` — Sayısal puan türü programları
- `programs_ea.json` — Eşit Ağırlık programları
- `programs_soz.json` — Sözel puan türü programları
- `programs_dil.json` — Dil puan türü programları
- `departments.json` — Bölüm istatistikleri
- `meta.json` — Üniversite/şehir listeleri ve özet
- `rank_history.json` — Başarı sırası trendi (varsa)

### Yasal & Mali Parametreler (`parametreler/`)

Asgari ücret, vergi dilimleri, SGK tavanı, kıdem tazminatı tavanı, MTV, KDV ve daha fazlası.

## Kullanım

### jsDelivr CDN ile (Önerilen)

```javascript
const CDN = 'https://cdn.jsdelivr.net/gh/KULLANICI/acik-veri@main';

// YKS 2026 SAY programları
const res = await fetch(`${CDN}/yks/2026/programs_say.json`);
const programs = await res.json();

// 2025 yasal parametreler
const params = await fetch(`${CDN}/parametreler/2025.json`).then(r => r.json());
```

### Ham GitHub URL ile (Fallback)

```javascript
const RAW = 'https://raw.githubusercontent.com/KULLANICI/acik-veri/main';
const data = await fetch(`${RAW}/yks/2026/meta.json`).then(r => r.json());
```

## Yeni Veri Ekleme

1. Ham ÖSYM Excel dosyasını temin edin
2. Dönüştürme betiğini çalıştırın:
   ```bash
   python scripts/convert_yks.py --t3 tablo3.xlsx --t4 tablo4.xlsx --year 2027 --out .
   ```
3. `manifest.json` dosyasını güncelleyin
4. `git push` yapın — jsDelivr birkaç dakika içinde güncellenir

## Lisans

Bu depodaki veriler ÖSYM ve ilgili resmi kurumlar tarafından kamuya açık olarak yayımlanmış bilgilerden derlenmiştir. Bilgilendirme amaçlıdır, resmi evrak yerine geçmez.
