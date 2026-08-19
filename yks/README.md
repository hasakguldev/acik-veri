# 🎓 YKS Üniversite Taban Puanları, Başarı Sıraları & Kontenjan Veri Seti (2022-2026)

Bu dizin, ÖSYM YKS (Yükseköğretim Kurumları Sınavı) merkezi yerleştirme verilerini içerir. Türkiye'deki 228 devlet, vakıf ve KKTC üniversitesinin tüm lisans ve ön lisans programları 5 yıllık başarı sırası ve taban puan geçmişiyle normalize edilmiştir.

## 📊 Puan Türlerine Göre Dosyalar ve CDN Bağlantıları

| Puan Türü | Kapsanan Alanlar | Program Sayısı | JSON CDN URL |
|---|---|---|---|
| **SAY** | Tıp, Diş Hekimliği, Mühendislik, Mimarlık, Fen | **5.757** | `https://cdn.jsdelivr.net/gh/hasakguldev/acik-veri@main/yks/programs_say.json` |
| **EA** | Hukuk, Psikoloji, İşletme, İktisat, PDR | **4.178** | `https://cdn.jsdelivr.net/gh/hasakguldev/acik-veri@main/yks/programs_ea.json` |
| **SÖZ** | İlahiyat, İletişim, Özel Eğitim, Tarih, Coğrafya | **1.980** | `https://cdn.jsdelivr.net/gh/hasakguldev/acik-veri@main/yks/programs_soz.json` |
| **DİL** | İngiliz Dili, Mütercim-Tercümanlık, Dilbilim | **709** | `https://cdn.jsdelivr.net/gh/hasakguldev/acik-veri@main/yks/programs_dil.json` |
| **TYT** | 2 Yıllık Ön Lisans / Meslek Yüksekokulları | **9.862** | `https://cdn.jsdelivr.net/gh/hasakguldev/acik-veri@main/yks/programs_tyt.json` |
| **Bölümler** | 957 Kanonik Bölüm Özeti (Min-Max Puanlar) | **957** | `https://cdn.jsdelivr.net/gh/hasakguldev/acik-veri@main/yks/departments.json` |
| **Metaveri** | 228 Üniversite ve 40 Şehir Kataloğu | Meta | `https://cdn.jsdelivr.net/gh/hasakguldev/acik-veri@main/yks/meta.json` |

## 🔍 Veri Alanları Açıklaması

- `code`: ÖSYM 9 haneli benzersiz program kodu (Örn: `106510077`)
- `univType`: Üniversite Türü (`DEVLET` | `VAKIF` | `KKTC` | `YABANCI`)
- `university`: Üniversite Adı
- `city`: Üniversitenin Bulunduğu İl
- `faculty`: Fakülte veya Yüksekokul Adı
- `program`: Bölüm / Program Adı
- `scoreType`: Puan Türü (`SAY`, `EA`, `SOZ`, `DIL`, `TYT`)
- `scholarship`: Burs Durumu (`none`, `full`, `50`, `25`, `75`)
- `language`: Öğretim Dili ISO Kodu (`tr`, `en`, `de`, `fr` vb.)
- `eduType`: Öğretim Türü (`formal` = Örgün, `distance` = Açık/Uzaktan, `evening` = İkinci Öğretim)
- `latest`: En son yerleştirme yılına ait kontenjan, yerleşen, taban puan ve sıralama
- `history`: 2026, 2025, 2024, 2023 ve 2022 yıllarına ait sıralı geçmiş dizisi
- `rankTrend`: Başarı sırası trendi (`up` = Yükseliyor/Zorlaşıyor, `down` = Düşüyor, `flat` = Yatay)
- `projectedRank`: Tahmini başarı sırası beklentisi
