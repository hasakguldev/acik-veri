# acik-veri

Türkiye eğitim, sınav, finans ve mevzuat verilerini içeren **merkezi açık veri deposu**.

Bu repo, birden fazla projenin (**Sitematik**, **enakillitercih / YKS Tercih Botu** ve gelecekteki projeler) ortak veri kaynağı olarak kullanılması için tasarlanmıştır. Veriler **jsDelivr CDN** üzerinden ücretsiz, yüksek hızlı ve CORS-uyumlu olarak dağıtılır.

---

## 🎯 Veri Modeli: Birleşik Program & Çok Yıllı Geçmiş (History Array)

Bu depoda her üniversite programı **tek ve benzersiz bir program nesnesi** olarak tutulur. Üniversite adı, bölüm adı, şehir ve fakülte gibi sabit metinler tekrarlanmaz. Yıllara ait kontenjan, yerleşen, taban puan ve başarı sıraları `history` dizisinde saklanır:

```json
{
  "code": "106510077",
  "univType": "DEVLET",
  "university": "ABDULLAH GÜL ÜNİVERSİTESİ",
  "city": "KAYSERİ",
  "faculty": "Mühendislik Fakültesi",
  "program": "Bilgisayar Mühendisliği",
  "scoreType": "SAY",
  "scholarship": "none",
  "language": "en",
  "eduType": "formal",
  "latest": {
    "year": 2026,
    "quota": 80,
    "placed": 80,
    "minScore": 442.53,
    "maxScore": 504.08,
    "minRank": 46890
  },
  "history": [
    { "year": 2026, "quota": 80, "placed": 80, "minScore": 442.53, "maxScore": 504.08, "minRank": 46890 },
    { "year": 2025, "quota": 80, "placed": 80, "minScore": 442.53, "maxScore": 504.08, "minRank": 46890 },
    { "year": 2024, "quota": 80, "placed": 80, "minScore": 471.55, "maxScore": null, "minRank": 39283 },
    { "year": 2023, "quota": 70, "placed": 70, "minScore": 455.20, "maxScore": null, "minRank": 41200 },
    { "year": 2022, "quota": 60, "placed": 60, "minScore": 435.10, "maxScore": null, "minRank": 45120 }
  ],
  "rankTrend": "flat",
  "projectedRank": 46890
}
```

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

### 2. Yasal & Mali Parametreler (`parametreler/`)

Asgari ücret, vergi dilimleri (GVK 103), SGK tavanı, kıdem tazminatı tavanı, MTV tarifesi, KDV oranları, faiz oranları vb.

- `parametreler/2025.json`

---

## 🚀 Kullanım (Hızlı Başlangıç)

### CDN Üzerinden Doğrudan Çekme (jsDelivr)

```javascript
const CDN = 'https://cdn.jsdelivr.net/gh/hasakguldev/acik-veri@main';

// 1. Sayısal programlarını çek (En son veriler + 5 yıllık geçmiş tek dosyada!)
const sayPrograms = await fetch(`${CDN}/yks/programs_say.json`).then(r => r.json());

// Örnek kullanım:
sayPrograms.forEach(prog => {
  console.log(`${prog.university} - ${prog.program}`);
  console.log(`Güncel Taban: ${prog.latest.minScore} | Sıralama: ${prog.latest.minRank}`);
  console.log(`Geçmiş Yıllar:`, prog.history);
});

// 2. Yasal parametreleri çek
const params2025 = await fetch(`${CDN}/parametreler/2025.json`).then(r => r.json());
console.log(`Brüt Asgari Ücret: ${params2025.asgariUcret.brut} TL`);
```

---

## 🛠️ Yeni Veri Ekleme & Güncelleme

Yeni bir ÖSYM kılavuzu yayımlandığında:
1. Excel dosyalarını temin edin.
2. `scripts/build_unified_yks.py` betiğini çalıştırın.
3. `git add . && git commit -m "feat: 2027 verisi eklendi" && git push`
4. Tüm projeler kod değiştirmeden saniyeler içinde güncellenir! ✨
