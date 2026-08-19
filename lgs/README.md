# 🏫 LGS Lise Taban Puanları ve Özel Yetenek Okulları Veri Seti (2026)

Bu dizin, MEB (Millî Eğitim Bakanlığı) e-Okul Liselere Geçiş Sistemi (LGS) ve Yetenek Sınavı ile öğrenci alan ortaöğretim kurumlarının tüm taban puanlarını, kontenjanlarını ve pansiyon bilgilerini içerir.

## 📊 Okul Türlerine Göre Dosyalar ve CDN Bağlantıları

| Dosya | Okul Türü | Sayı | Açıklama |
|---|---|---|---|
| [`schools.json`](https://cdn.jsdelivr.net/gh/hasakguldev/acik-veri@main/lgs/schools.json) | Tüm Liseler | **3.154** | 81 İldeki merkezi sınavla alan tüm liseler |
| [`schools_fen.json`](https://cdn.jsdelivr.net/gh/hasakguldev/acik-veri@main/lgs/schools_fen.json) | Fen Liseleri | **383** | Devlet ve Proje Fen Liseleri |
| [`schools_anadolu.json`](https://cdn.jsdelivr.net/gh/hasakguldev/acik-veri@main/lgs/schools_anadolu.json) | Anadolu Liseleri | **532** | Proje ve Hazırlık Sınıflı Anadolu Liseleri |
| [`schools_imamhatip.json`](https://cdn.jsdelivr.net/gh/hasakguldev/acik-veri@main/lgs/schools_imamhatip.json) | İmam Hatip | **854** | Fen ve Sosyal Bilimler Proje AİHL |
| [`schools_meslek.json`](https://cdn.jsdelivr.net/gh/hasakguldev/acik-veri@main/lgs/schools_meslek.json) | Mesleki Teknik | **1.276** | ATP ve AMP Mesleki Anadolu Liseleri |
| [`schools_sosyal.json`](https://cdn.jsdelivr.net/gh/hasakguldev/acik-veri@main/lgs/schools_sosyal.json) | Sosyal Bilimler | **109** | Sosyal Bilimler Liseleri |
| [`yetenek_okullari.json`](https://cdn.jsdelivr.net/gh/hasakguldev/acik-veri@main/lgs/yetenek_okullari.json) | Yetenek Liseleri | **504** | Özel Yetenekle Öğrenci Alan Tüm Kurumlar |
| [`yetenek_guzelsanatlar.json`](https://cdn.jsdelivr.net/gh/hasakguldev/acik-veri@main/lgs/yetenek_guzelsanatlar.json)| Güzel Sanatlar | **225** | Resim, Müzik, Tiyatro, Sinema Liseleri |
| [`yetenek_spor.json`](https://cdn.jsdelivr.net/gh/hasakguldev/acik-veri@main/lgs/yetenek_spor.json) | Spor Liseleri | **121** | Genel ve Tematik Spor Liseleri |
| [`yetenek_imamhatip.json`](https://cdn.jsdelivr.net/gh/hasakguldev/acik-veri@main/lgs/yetenek_imamhatip.json) | Musiki/Hafızlık | **158** | Musiki, Hafızlık, Hat/Tezhip Proje AİHL |
| [`meta.json`](https://cdn.jsdelivr.net/gh/hasakguldev/acik-veri@main/lgs/meta.json) | Metaveri | Meta | 81 İl ve 549 İlçe Haritası |

## 🔍 Veri Formatı

```json
{
  "code": "24843",
  "city": "İSTANBUL",
  "district": "KADIKÖY",
  "school": "İstanbul Atatürk Fen Lisesi",
  "schoolType": "Hazırlık Sınıfı Bulunan Fen Lisesi",
  "category": "fen",
  "field": "FEN BİLİMLERİ ALANI (FEN LİS.)",
  "duration": "Hazırlık + 4 yıl",
  "gender": "Kız/Erkek",
  "boarding": "Var (Erkek: 4, Kız: 4)",
  "language": "Almanca",
  "langCode": "de",
  "emptyQuota": 0,
  "minScore": 500.0,
  "scoreFirstPlacement": 500.0,
  "scoreSecondPlacement": 494.8872,
  "year": 2026
}
```
