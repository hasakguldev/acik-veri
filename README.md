# acik-veri

Türkiye eğitim, sınav, finans ve mevzuat verilerini içeren **merkezi açık veri deposu**.

Bu repo, birden fazla projenin (**Sitematik**, **enakillitercih / YKS Tercih Botu**, **LGS Tercih Rehberi**, **Yetenek Sınavı Sihirbazı** vb.) ortak veri kaynağı olarak kullanılması için tasarlanmıştır. Veriler **jsDelivr CDN** üzerinden ücretsiz, yüksek hızlı ve CORS-uyumlu olarak dağıtılır.

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

### 2. LGS Liseleri & Özel Yetenek Sınavı Okulları (`lgs/`)

MEB Merkezi Sınav ve Özel Yetenek Sınavı ile öğrenci alan liselerin taban puanları, kontenjanları ve pansiyon durumları.

| Dosya | Okul Türü | Okul/Program Sayısı |
|---|---|---|
| `lgs/schools.json` | Merkezi Sınav Tüm Liseler | **3.154** okul programı |
| `lgs/schools_fen.json` | Fen Liseleri | **383** lise |
| `lgs/schools_anadolu.json` | Anadolu Liseleri | **532** lise |
| `lgs/schools_imamhatip.json` | Anadolu İmam Hatip Liseleri | **854** lise |
| `lgs/schools_meslek.json` | Mesleki ve Teknik Liseler | **1.276** program |
| `lgs/schools_sosyal.json` | Sosyal Bilimler Liseleri | **109** lise |
| `lgs/yetenek_okullari.json` | **Özel Yetenekle Alan Tüm Liseler** | **504** okul programı |
| `lgs/yetenek_guzelsanatlar.json`| **Güzel Sanatlar Liseleri** (Resim/Müzik/Tiyatro) | **225** okul programı |
| `lgs/yetenek_spor.json` | **Spor Liseleri** (Genel & Tematik) | **121** okul programı |
| `lgs/yetenek_imamhatip.json` | **Musiki / Hafızlık / Sanat AİHL** | **158** okul programı |

### 3. Yasal & Mali Parametreler (`parametreler/`)

Asgari ücret, vergi dilimleri (GVK 103), SGK tavanı, kıdem tazminatı tavanı, MTV tarifesi, KDV oranları, faiz oranları vb.

- `parametreler/2025.json`

---

## 🚀 Kullanım (Hızlı Başlangıç)

### CDN Üzerinden Doğrudan Çekme (jsDelivr)

```javascript
const CDN = 'https://cdn.jsdelivr.net/gh/hasakguldev/acik-veri@main';

// 1. Güzel Sanatlar Liselerini çek
const gsLiseleri = await fetch(`${CDN}/lgs/yetenek_guzelsanatlar.json`).then(r => r.json());
console.log(`Güzel Sanatlar Lisesi Program Sayısı: ${gsLiseleri.length}`);

// 2. Spor Liselerini çek
const sporLiseleri = await fetch(`${CDN}/lgs/yetenek_spor.json`).then(r => r.json());

// 3. LGS Fen Liselerini çek
const fenLiseleri = await fetch(`${CDN}/lgs/schools_fen.json`).then(r => r.json());
```
