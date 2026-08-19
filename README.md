# acik-veri

Türkiye eğitim, sınav, finans ve mevzuat verilerini içeren **merkezi açık veri deposu**.

Bu repo, birden fazla projenin (**Sitematik**, **enakillitercih / YKS Tercih Botu**, **LGS Tercih Robotu** ve gelecekteki projeler) ortak veri kaynağı olarak kullanılması için tasarlanmıştır. Veriler **jsDelivr CDN** üzerinden ücretsiz, yüksek hızlı ve CORS-uyumlu olarak dağıtılır.

---

## 📁 Veri Setleri

### 1. YKS Üniversite Yerleştirme Verileri (`yks/`)

ÖSYM YKS merkezi yerleştirme taban/tavan puanları, kontenjanlar, 5 yıllık başarı sıraları ve bölüm istatistikleri.

| Dosya | Puan Türü | Benzersiz Program Sayısı |
|---|---|---|
| `yks/programs_tyt.json` | TYT (Ön Lisans) | 9.862 program |
| `yks/programs_say.json` | Sayısal (SAY) | 5.757 program |
| `yks/programs_ea.json` | Eşit Ağırlık (EA) | 4.178 program |
| `yks/programs_soz.json` | Sözel (SÖZ) | 1.980 program |
| `yks/programs_dil.json` | Dil (DİL) | 709 program |
| `yks/departments.json` | Tüm Bölümler | 957 kanonik bölüm |
| `yks/meta.json` | Metaveri | 228 üniversite, 40 şehir |

### 2. LGS Lise Taban Puanları & Tercih Verileri (`lgs/`)

MEB Merkezi Sınav ile öğrenci alan liselerin taban puanları, pansiyon durumları, öğretim şekilleri ve boş kontenjanları.

| Dosya | Okul Türü | Okul/Program Sayısı |
|---|---|---|
| `lgs/schools.json` | Tüm Liseler (Genel Liste) | **3.154** okul programı |
| `lgs/schools_fen.json` | Fen Liseleri | **383** lise |
| `lgs/schools_anadolu.json` | Anadolu Liseleri | **532** lise |
| `lgs/schools_imamhatip.json` | Anadolu İmam Hatip Liseleri | **854** lise |
| `lgs/schools_meslek.json` | Mesleki ve Teknik Anadolu Liseleri | **1.276** program |
| `lgs/schools_sosyal.json` | Sosyal Bilimler Liseleri | **109** lise |
| `lgs/departments.json` | Mesleki & Teknik Alanlar | **94** alan/bölüm |
| `lgs/meta.json` | Metaveri | **81 İl**, **549 İlçe** |

### 3. Yasal & Mali Parametreler (`parametreler/`)

Asgari ücret, vergi dilimleri (GVK 103), SGK tavanı, kıdem tazminatı tavanı, MTV tarifesi, KDV oranları, faiz oranları vb.

- `parametreler/2025.json`

---

## 🚀 Kullanım (Hızlı Başlangıç)

### CDN Üzerinden Doğrudan Çekme (jsDelivr)

```javascript
const CDN = 'https://cdn.jsdelivr.net/gh/hasakguldev/acik-veri@main';

// 1. LGS Fen Liselerini çek
const fenLiseleri = await fetch(`${CDN}/lgs/schools_fen.json`).then(r => r.json());
console.log(`Toplam Fen Lisesi: ${fenLiseleri.length}`);

// 2. YKS Sayısal programlarını çek (En son veriler + 5 yıllık geçmiş tek dosyada!)
const sayPrograms = await fetch(`${CDN}/yks/programs_say.json`).then(r => r.json());

// 3. Yasal parametreleri çek
const params2025 = await fetch(`${CDN}/parametreler/2025.json`).then(r => r.json());
```

---

## 🛠️ Yeni Veri Ekleme & Güncelleme

Yeni bir ÖSYM veya MEB kılavuzu yayımlandığında:
1. Excel dosyalarını temin edin.
2. İlgili dönüştürücü betiği çalıştırın (`scripts/convert_yks.py` veya `scripts/convert_lgs.py`).
3. `git add . && git commit -m "feat: veri seti güncellendi" && git push`
4. Tüm projeler saniyeler içinde CDN üzerinden güncellenir! ✨
