import os
import json
import datetime
import yfinance as yf

def fetch_live_data():
    """
    Yahoo Finance üzerinden anlık finansal kurları çeker.
    Dolar, Euro, Sterlin, Altın, Gümüş, Bitcoin ve BIST100 verilerini alır.
    """
    tickers = {
        "USDTRY": "USDTRY=X",    # Dolar
        "EURTRY": "EURTRY=X",    # Euro
        "GBPTRY": "GBPTRY=X",    # Sterlin
        "GOLD": "GC=F",          # Ons Altın
        "SILVER": "SI=F",        # Ons Gümüş
        "BTC": "BTC-USD",        # Bitcoin
        "BIST100": "XU100.IS"    # Borsa İstanbul 100 Endeksi
    }
    
    data = {}
    
    for name, ticker in tickers.items():
        try:
            ticker_data = yf.Ticker(ticker)
            # 1 günlük geçmişi al ve son kapanış fiyatını kullan
            hist = ticker_data.history(period="1d")
            if not hist.empty:
                current_price = hist['Close'].iloc[-1]
                data[name] = round(current_price, 4)
            else:
                data[name] = None
                print(f"Uyarı: {name} için veri alınamadı.")
        except Exception as e:
            print(f"Hata: {name} verisi çekilirken bir sorun oluştu - {e}")
            data[name] = None

    # Türetilmiş Veriler (Gram Altın ve Gram Gümüş)
    # 1 Ons = 31.1034768 Gram.
    if data.get("GOLD") is not None and data.get("USDTRY") is not None:
        data["GRAM_ALTIN"] = round((data["GOLD"] / 31.1034768) * data["USDTRY"], 2)
        
    if data.get("SILVER") is not None and data.get("USDTRY") is not None:
        data["GRAM_GUMUS"] = round((data["SILVER"] / 31.1034768) * data["USDTRY"], 2)

    # JSON yapısını oluştur
    output = {
        "son_guncelleme": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "kaynak": "Yahoo Finance",
        "kurlar": data
    }
    
    # Çıktı dosyasının yazılacağı dizin
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    finans_dir = os.path.join(base_dir, "finans")
    os.makedirs(finans_dir, exist_ok=True)
    
    out_file = os.path.join(finans_dir, "canli-kurlar.json")
    
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
        
    print(f"[OK] Canlı kurlar başarıyla güncellendi: {out_file}")

if __name__ == "__main__":
    fetch_live_data()
