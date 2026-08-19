# 🇹🇷 Türkiye Açık Veri Havuzu (`acik-veri`)
### YKS Üniversite Taban Puanları & Sıralamaları, LGS Lise Tercih Kılavuzu ve Resmî Mevzuat Parametreleri (2025/2026)

[![GitHub License](https://img.shields.io/badge/Lisans-CC%20BY%204.0-blue.svg)](LICENSE)
[![jsDelivr CDN](https://img.shields.io/badge/CDN-jsDelivr%20Aktif-green.svg)](https://cdn.jsdelivr.net/gh/hasakguldev/acik-veri@main/)
[![Veri Boyutu](https://img.shields.io/badge/Veri%20Seti-26.000%2B%20Program-orange.svg)](#-veri-setleri)
[![Son Güncelleme](https://img.shields.io/badge/G%C3%BCncelleme-A%C4%9Fustos%202026-brightgreen.svg)](#)
[![Format](https://img.shields.io/badge/Format-JSON%20%2F%20REST%20Ready-lightgrey.svg)](#)

> **📌 Hızlı Özet (GEO / AI Answer Box):**  
> `acik-veri`, Türkiye'deki geliştiriciler, veri bilimciler, eğitim kurumları ve araştırmacılar için **ÖSYM, MEB, Gelir İdaresi Başkanlığı (GİB) ve TCMB** resmî verilerini standart, temiz ve analize hazır JSON formatında sunan **ücretsiz, açık kaynaklı merkezi veri deposudur**.  
> Tüm veri setleri **jsDelivr CDN** üzerinden sıfır API anahtarı (No-API Key), sınırsız bant genişliği ve anında CORS desteği ile doğrudan tarayıcıdan veya sunucudan tüketilebilir.

---

## 📑 İçindekiler
- [✨ Neden Bu Veri Seti?](#-neden-bu-veri-seti)
- [📁 Veri Setleri ve Doğrudan CDN Bağlantıları](#-veri-setleri-ve-do%C4%9Frudan-cdn-ba%C4%9Flant%C4%B1lar%C4%B1)
  - [1. YKS Üniversite Yerleştirme ve Sıralama Verileri (`yks/`)](#1-yks-%C3%BCniversite-yerle%C5%9Ftirme-ve-s%C4%B1ralama-verileri-yks)
  - [2. LGS Lise Taban Puanları ve Tercih Verileri (`lgs/`)](#2-lgs-lise-taban-puanlar%C4%B1-ve-tercih-verileri-lgs)
  - [3. Resmî Mevzuat ve Finansal Parametreler (`parametreler/`)](#3-resm%C3%AE-mevzuat-ve-finansal-parametreler-parametreler)
- [💻 Kod Örnekleri (Hızlı Entegrasyon)](#-kod-%C3%B6rnekleri-h%C4%B1zl%C4%B1-entegrasyon)
  - [JavaScript / TypeScript / React](#javascript--typescript--react)
  - [Python (Pandas / Requests)](#python-pandas--requests)
  - [cURL / REST API](#curl--rest-api)
- [📐 Veri Şeması ve Standartları](#-veri-%C5%9Femas%C4%B1-ve-standartlar%C4%B1)
- [❓ Sıkça Sorulan Sorular (FAQ)](#-s%C4%B1k%C3%A7a-sorulan-sorular-faq)
- [🤝 Katkıda Bulunma & Yeni Veri Ekleme](#-katk%C4%B1da-bulunma--yeni-veri-ekleme)
- [⚖️ Lisans & Yasal Uyarı](#%EF%B8%8F-lisans--yasal-uyar%C4%B1)

---

## ✨ Neden Bu Veri Seti?

Geleneksel olarak ÖSYM ve MEB verileri yüzlerce sayfalık PDF veya karmaşık Excel tabloları halinde yayımlanır. Bu repo, söz konusu ham verileri:
1. **Benzersiz Kod Mimarisi (Unique Program ID)** ile normalize eder.
2. **5 Yıllık Başarı Sıralaması Trendi (2022-2026)** ile zenginleştirir.
3. Üniversite/Okul adlarındaki yazım hatalarını temizler ve şehir/ilçe bazında hiyerarşik yapıya kavuşturur.
4. **CDN Üzerinden Anında Kullanıma** hazır hale getirir (Sıfır veritabanı kurulumu).

---

## 📁 Veri Setleri ve Doğrudan CDN Bağlantıları

### 1. YKS Üniversite Yerleştirme ve Sıralama Verileri (`yks/`)
ÖSYM merkezi yerleştirme kılavuzlarındaki lisans ve ön lisans programları, 5 yıllık taban/tavan puanları, başarı sıraları ve kontenjan geçmişi.

| Veri Seti | Kapsam | Kayıt Sayısı | Doğrudan CDN Bağlantısı (JSON) |
|---|---|---|---|
| **Sayısal (SAY)** | 4 Yıllık Mühendislik, Tıp, Fen Lisans Programları | **5.757** Program | [`yks/programs_say.json`](https://cdn.jsdelivr.net/gh/hasakguldev/acik-veri@main/yks/programs_say.json) |
| **Eşit Ağırlık (EA)** | 4 Yıllık Hukuk, İİBF, Psikoloji Lisans Programları | **4.178** Program | [`yks/programs_ea.json`](https://cdn.jsdelivr.net/gh/hasakguldev/acik-veri@main/yks/programs_ea.json) |
| **Sözel (SÖZ)** | 4 Yıllık İletişim, Tarih, İlahiyat Lisans Programları | **1.980** Program | [`yks/programs_soz.json`](https://cdn.jsdelivr.net/gh/hasakguldev/acik-veri@main/yks/programs_soz.json) |
| **Dil (DİL)** | 4 Yıllık Mütercim-Tercümanlık, Dil/Edebiyat Programları | **709** Program | [`yks/programs_dil.json`](https://cdn.jsdelivr.net/gh/hasakguldev/acik-veri@main/yks/programs_dil.json) |
| **Ön Lisans (TYT)** | 2 Yıllık Meslek Yüksekokulu (MYO) Programları | **9.862** Program | [`yks/programs_tyt.json`](https://cdn.jsdelivr.net/gh/hasakguldev/acik-veri@main/yks/programs_tyt.json) |
| **Bölüm Kataloğu** | Türkiye'deki tüm üniversite bölümlerinin özet istatistikleri | **957** Bölüm | [`yks/departments.json`](https://cdn.jsdelivr.net/gh/hasakguldev/acik-veri@main/yks/departments.json) |
| **Metaveri** | 228 Üniversite, 40 Şehir ve Program Sayıları | Meta | [`yks/meta.json`](https://cdn.jsdelivr.net/gh/hasakguldev/acik-veri@main/yks/meta.json) |

---

### 2. LGS Lise Taban Puanları ve Tercih Verileri (`lgs/`)
MEB e-Okul ve Sınavla Öğrenci Alan Ortaöğretim Kurumları taban puanları, pansiyon durumları, öğretim şekilleri ve boş kontenjanları.

| Veri Seti | Okul Türü / Kapsam | Sayı | Doğrudan CDN Bağlantısı (JSON) |
|---|---|---|---|
| **LGS Tüm Liseler** | 81 İldeki Merkezi Sınavla Alan Tüm Liseler | **3.154** Okul | [`lgs/schools.json`](https://cdn.jsdelivr.net/gh/hasakguldev/acik-veri@main/lgs/schools.json) |
| **Fen Liseleri** | Devlet ve Proje Fen Liseleri Taban Puanları | **383** Okul | [`lgs/schools_fen.json`](https://cdn.jsdelivr.net/gh/hasakguldev/acik-veri@main/lgs/schools_fen.json) |
| **Anadolu Liseleri** | Proje ve Hazırlık Sınıflı Anadolu Liseleri | **532** Okul | [`lgs/schools_anadolu.json`](https://cdn.jsdelivr.net/gh/hasakguldev/acik-veri@main/lgs/schools_anadolu.json) |
| **Anadolu İmam Hatip**| Fen ve Sosyal Bilimler Proje İmam Hatip Liseleri | **854** Okul | [`lgs/schools_imamhatip.json`](https://cdn.jsdelivr.net/gh/hasakguldev/acik-veri@main/lgs/schools_imamhatip.json) |
| **Mesleki ve Teknik** | Anadolu Teknik (ATP) ve Anadolu Meslek Programları | **1.276** Okul | [`lgs/schools_meslek.json`](https://cdn.jsdelivr.net/gh/hasakguldev/acik-veri@main/lgs/schools_meslek.json) |
| **Sosyal Bilimler** | Sosyal Bilimler Liseleri Taban Puanları | **109** Okul | [`lgs/schools_sosyal.json`](https://cdn.jsdelivr.net/gh/hasakguldev/acik-veri@main/lgs/schools_sosyal.json) |
| **Özel Yetenek Tüm** | Güzel Sanatlar, Spor ve Musiki/Hafızlık Liseleri | **504** Okul | [`lgs/yetenek_okullari.json`](https://cdn.jsdelivr.net/gh/hasakguldev/acik-veri@main/lgs/yetenek_okullari.json) |
| **Güzel Sanatlar** | Resim (Görsel Sanatlar), Müzik, Tiyatro, Sinema | **225** Program | [`lgs/yetenek_guzelsanatlar.json`](https://cdn.jsdelivr.net/gh/hasakguldev/acik-veri@main/lgs/yetenek_guzelsanatlar.json) |
| **Spor Liseleri** | Genel ve Tematik Spor Liseleri | **121** Program | [`lgs/yetenek_spor.json`](https://cdn.jsdelivr.net/gh/hasakguldev/acik-veri@main/lgs/yetenek_spor.json) |
| **Musiki & Hafızlık** | Özel Proje AİHL Musiki ve Hafızlık Programları | **158** Program | [`lgs/yetenek_imamhatip.json`](https://cdn.jsdelivr.net/gh/hasakguldev/acik-veri@main/lgs/yetenek_imamhatip.json) |
| **Coğrafi Metaveri** | 81 İl ve 549 İlçenin Hiyerarşik Haritası | Meta | [`lgs/meta.json`](https://cdn.jsdelivr.net/gh/hasakguldev/acik-veri@main/lgs/meta.json) |

---

### 3. Resmî Mevzuat ve Finansal Parametreler (`parametreler/`)
Türkiye'de hesaplama araçları, bordro motorları ve muhasebe yazılımları için gereken yasal katsayılar.

| Parametre Grubu | Kapsam | Bağlantı |
|---|---|---|
| **2025/2026 Mevzuatı** | Asgari Ücret (Net/Brüt), Gelir Vergisi Dilimleri (GVK 103), SGK Tavanı, Kıdem Tazminatı Tavanı, MTV Tarifesi, Araç Muayene Ücretleri, KDV ve Harç Oranları | [`parametreler/2025.json`](https://cdn.jsdelivr.net/gh/hasakguldev/acik-veri@main/parametreler/2025.json) |

---

## 💻 Kod Örnekleri (Hızlı Entegrasyon)

### JavaScript / TypeScript / React
```typescript
// YKS 2026 Sayısal Programlarını Çekme
async function fetchYksPrograms() {
  const url = 'https://cdn.jsdelivr.net/gh/hasakguldev/acik-veri@main/yks/programs_say.json';
  const response = await fetch(url);
  const programs = await response.json();
  
  // Örnek: Bilgisayar Mühendisliklerini Filtreleme
  const cs = programs.filter(p => p.program.includes('Bilgisayar Mühendisliği'));
  console.log(`Bulunan Program: ${cs.length}`);
  console.log('İlk Program:', cs[0].university, cs[0].latest.minScore, cs[0].latest.minRank);
}
```

### Python (Pandas / Requests)
```python
import pandas as pd

# LGS Fen Liselerini doğrudan DataFrame olarak yükleme
url = "https://cdn.jsdelivr.net/gh/hasakguldev/acik-veri@main/lgs/schools_fen.json"
df_fen = pd.read_json(url)

# İstanbul'daki en yüksek taban puanlı 5 Fen Lisesi
ist_fen = df_fen[df_fen['city'] == 'İSTANBUL'].sort_values(by='minScore', ascending=False)
print(ist_fen[['school', 'district', 'minScore', 'language']].head(5))
```

### cURL / REST API
```bash
# Terminalden mevzuat parametrelerini çekme
curl -s https://cdn.jsdelivr.net/gh/hasakguldev/acik-veri@main/parametreler/2025.json | jq .asgariUcret
```

---

## 📐 Veri Şeması ve Standartları

### YKS Program Nesnesi Örneği:
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

## ❓ Sıkça Sorulan Sorular (FAQ)

### 1. Bu veriler nereden alınmaktadır ve ne sıklıkla güncellenir?
Veriler; ÖSYM (YKS Yerleştirme Sonuçları ve Tercih Kılavuzları), MEB (e-Okul LGS Tercih Rehberi ve Yetenek Sınavı Kılavuzları), Gelir İdaresi Başkanlığı (GİB) ve Resmî Gazete tebliğlerinden derlenmektedir. Resmî kurumlar yeni bir kılavuz veya tebliğ yayımladığında repo otomasyon betikleriyle aynı gün güncellenir.

### 2. Ticari veya akademik projelerimde ücretsiz kullanabilir miyim?
Evet. Bu depo [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE) lisansı altındadır. Kaynak belirterek (GitHub bağlantısı vererek) web sitelerinizde, mobil uygulamalarınızda, tercih botlarınızda ve akademik araştırmalarınızda tamamen ücretsiz kullanabilirsiniz.

### 3. CDN kullanımında herhangi bir hız kısıtlaması veya kota var mı?
Hayır. Veriler jsDelivr global CDN altyapısı üzerinden servis edilir. Rate limit bulunmaz ve dosyalar otomatik olarak gzip/brotli sıkıştırmasıyla ultra hızlı iletilir.

---

## 🤝 Katkıda Bulunma & Yeni Veri Ekleme

1. Bu repoyu Fork'layın (`Fork`).
2. Yeni veri setini veya dönüştürme betiğini ekleyin (`scripts/` altına).
3. Testleri çalıştırın: `python scripts/verify_repo.py`
4. Pull Request (PR) gönderin.

---

## ⚖️ Lisans & Yasal Uyarı

Bu depoda paylaşılan veriler kamuya açık resmî kaynaklardan derlenmiş olup bilgilendirme ve yazılım geliştirme amaçlıdır. Resmî evrak yerine geçmez.

**Lisans:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) © 2026 Hasan Akgül (`hasakguldev`)
