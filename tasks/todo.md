# Canlı Finansal Veri Otomasyonu (Günde 10 Kez)

## Plan (Canlı Kurlar)
- [x] `scripts/fetch_live_rates.py` dosyasını oluştur (Yahoo Finance üzerinden Dolar, Euro, Altın).
- [x] `.github/workflows/canli-veri-guncelle.yml` dosyasını oluştur (GitHub Actions otomasyonu).
- [x] Betiğin lokal olarak çalıştığını ve `finans/canli-kurlar.json` dosyasını ürettiğini test et.

## Plan (Tarihsel Veriler ve Mimari Çözüm)
- [x] Manuel (Pasaport vb.) veriler, tarihsel hesaplamalar ve canlı veriler için mimari planlama yap.
- [x] `.github/workflows/tarihsel-veri-guncelle.yml` oluştur (Haftalık EVDS arşivi).
- [x] GitHub Secrets (`EVDS_API_KEY`) entegrasyonu ve güvenlik prosedürlerini dokümante et.
- [x] **Ekstra İstek:** BIST100 ve BTC'nin 10 yıllık geçmişini `fetch_evds.py` arşivine yfinance üzerinden dahil et.

## Review
Tüm planlama başarıyla uygulandı:
- Anlık kurları Yahoo Finance'den çeken `fetch_live_rates.py` betiği oluşturuldu ve sonradan genişletildi.
- Artık betik şu kurları çekiyor: Dolar (USDTRY), Euro (EURTRY), Sterlin (GBPTRY), Ons Altın (GOLD), Ons Gümüş (SILVER), Bitcoin (BTC), ve Borsa İstanbul (BIST100).
- Bu veriler kullanılarak **Gram Altın** ve **Gram Gümüş** TL fiyatları dinamik olarak hesaplanıyor.
- `canli-kurlar.json` dosyası yeni eklemelerle başarıyla test edildi.
- GitHub Actions üzerinde mesai saatleri içinde her saat başı çalışacak bir otomasyon (`canli-veri-guncelle.yml`) aktif edildi.
