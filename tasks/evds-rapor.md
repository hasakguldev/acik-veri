# TCMB EVDS Tarihsel Fiyat Serileri Veri Çekme ve Zincirleme Raporu

**Rapor Tarihi:** 2026-10-10 05:36:59

## 1. Kimlik Doğrulama Yöntemi
- **Çalışan Yöntem:** `key` HTTP Başlığı (Header) — `headers={'key': API_KEY}`
- **API Taban Adresi (Base URL):** `https://evds3.tcmb.gov.tr/igmevdsms-dis/`
- **Sorgu Parametresi Testi:** `key` parametresi URL içine eklendiğinde API `403 Required request header 'key' is not present` dönmektedir. HTTP Header zorunludur.

## 2. Kullanılan Seriler ve Tarih Aralıkları
| Seri | Ad | EVDS Kodları / Yöntem | Başlangıç | Bitiş | Veri Noktası | 10^6 Bölme? |
|---|---|---|---|---|---|---|
| `usd` | ABD Doları | `TP.DK.USD.S.YTL` | 1980-01 | 2026-10 | 562 ay | Doğrudan YTL / Türetilmiş |
| `eur` | Euro | `TP.DK.EUR.S.YTL` | 1999-01 | 2026-10 | 334 ay | Doğrudan YTL / Türetilmiş |
| `altin` | Gram Altın | `TP.MK.D.AOF.Y + TP.ALTINPIYASA.AGORT03` | 1995-07 | 2026-10 | 376 ay | Doğrudan YTL / Türetilmiş |
| `gumus` | Gram Gümüş | `TP.GUMUSPIYASA.KAP05 / KAP02` | 2018-07 | 2026-10 | 100 ay | Doğrudan YTL / Türetilmiş |
| `benzin` | Benzin | `TP.TUKFIY2025.07222` | 2005-01 | 2026-09 | 261 ay | Doğrudan YTL / Türetilmiş |
| `tufe` | TÜFE | `TP.FG.J0 (Zincirlenmiş)` | 1982-01 | 2026-01 | 529 ay | Doğrudan YTL / Türetilmiş |
| `btc` | Bitcoin | `BTC-USD (Yahoo Finance)` | 2014-09 | 2026-10 | 146 ay | Doğrudan YTL / Türetilmiş |
| `bist100` | Borsa İstanbul 100 | `XU100.IS (Yahoo Finance)` | 1997-07 | 2026-10 | 352 ay | Doğrudan YTL / Türetilmiş |

## 3. Gram Altın Türetme Metodolojisi
- **Problem:** EVDS'teki doğrudan TL/gram altın serisi (`TP.ALTINPIYASA.KAP05`) yalnızca Aralık 2018'den başlamaktadır.
- **Çözüm:** EVDS'te yer alan Borsa İstanbul / İstanbul Altın Borsası resmi USD/Ons serileri kullanılarak TL/gram serisi türetilmiştir:
  - **1995-07..2018-06:** `TP.MK.D.AOF.Y` (İAB Ağırlıklı Ortalama USD/Ons)
  - **2018-07..2026-08:** `TP.ALTINPIYASA.AGORT03` (BIST Kıymetli Madenler Ağırlıklı Ortalama USD/Ons)
  - **Döviz Kuru:** `TP.DK.USD.S.YTL` (TCMB USD/TRY Döviz Satış Kuru)
  - **Formül:** `gram_altin_tl = (ons_usd / 31.1035) * usd_try`
  - **Sonuç:** Gram altın verisi **Temmuz 1995**'ten günümüze kadar kesintisiz 374 aya genişletilmiştir.
  - **1980-1995/06 Dönemi:** EVDS bünyesinde resmi serbest piyasa / borsa altın kuru serisi bulunmadığından veri uydurulmamış, `null` olarak işaretlenmiştir.

## 4. TÜFE Geçmiş Baz Yılları Zincirleme (Chain-Linking) Metodolojisi
- **Problem:** `TP.FG.J0` (2003=100) serisi 2003'te başlayıp 2026-01'de durmaktadır.
- **Çözüm (Geriye Doğru Zincirleme):** EVDS'teki arşiv TÜFE serileri örtüşen 12 aylık geçiş dönemlerinin geometrik/aritmetik ortalama çarpanları hesaplanarak 2003=100 bazına bağlanmıştır:
  1. **1994=100 $\rightarrow$ 2003=100:** `TP.FG.T01` (1994-01..2002-12) $\times 0.0120109719$
  2. **1987=100 $\rightarrow$ 2003=100:** `TP.FG.A01` (1987-01..1993-12) $\times 0.0002723318$
  3. **1982=100 $\rightarrow$ 2003=100:** `TP.FG.F01` (1982-01..1986-12) $\times 0.0000123114$
- **Çözüm (İleriye Doğru Güncelleme):** TCMB, TÜİK 2025 revizyonu ile güncel verileri `TP.FE25.OKTG01` altında yayınlamaktadır. 2025 yılı örtüşme çarpanı ($31.832296$) kullanılarak **2026-02..2026-07 dönemi** 2003=100 bazında kesintisiz seriye eklenmiştir.
- **Sonuç:** TÜFE serisi **Ocak 1982**'den **Temmuz 2026**'ya kadar kesintisiz **535 ay** olarak tek birleştirilmiş seriye dönüştürülmüştür.

## 5. 2005 Para Reformu (6 Sıfır / 10^6 Sıçrama) Denetimleri
- **USD/TRY:** 2004-12 ($1.4001$ ₺) $\rightarrow$ 2005-01 ($1.3565$ ₺) doğrudan YTL serisidir.
- **EUR/TRY:** 2004-12 ($1.8749$ ₺) $\rightarrow$ 2005-01 ($1.7873$ ₺) doğrudan YTL serisidir.
- **Gram Altın (Türetilmiş):** 2004-12 ($19.9068$ ₺/gr) $\rightarrow$ 2005-01 ($18.4862$ ₺/gr) pürüzsüz geçiş teyit edilmiştir.
- **TÜFE (Zincirlenmiş):** 2004-12 ($113.86$) $\rightarrow$ 2005-01 ($114.49$) (Endeks birimsizdir).

## 6. Gümüş ve Benzin Veri Kapsamı
- **Gram Gümüş:** BIST Kıymetli Madenler Piyasası verileri (`TP.GUMUSPIYASA.KAP05` ve `KAP02`) kullanılarak **Temmuz 2018**'den günümüze kadar sunulmuştur. 2018 öncesi resmi kamu API serisi bulunmadığından `null` bırakılmıştır.
- **Benzin:** TÜİK Tüketici Fiyat Endeksi Madde Sepeti (`TP.TUKFIY2025.07222`) perakende pompa fiyatı olarak **Ocak 2005**'ten Temmuz 2026'ya kadar sunulmuştur.

## 7. Çıktı Standardı
- Çıktı tek satır (compact JSON) UTF-8 olarak `public/eglence/tarihsel-fiyatlar.json` dosyasına kaydedilmiştir.