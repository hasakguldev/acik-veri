import json
import os
import pandas as pd
import yfinance as yf

JSON_PATH = "finans/tarihsel-fiyatlar.json"

def main():
    if not os.path.exists(JSON_PATH):
        print(f"{JSON_PATH} bulunamadi!")
        return

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    print("Yahoo Finance'den BTC ve BIST100 gecmis verileri cekiliyor...")
    tickers = {"btc": "BTC-USD", "bist100": "XU100.IS"}
    yf_data = {"btc": {}, "bist100": {}}

    for key, symbol in tickers.items():
        try:
            tk = yf.Ticker(symbol)
            hist = tk.history(period="max")
            if not hist.empty:
                hist.index = pd.to_datetime(hist.index)
                monthly_avg = hist['Close'].resample('ME').mean()
                for date, val in monthly_avg.items():
                    d_key = f"{date.year:04d}-{date.month:02d}"
                    yf_data[key][d_key] = round(float(val), 4)
            print(f"   {key.upper()}: {len(yf_data[key])} ay cekildi.")
        except Exception as e:
            print(f"   Hata ({symbol}): {e}")

    # Metadata güncelle
    if "seriler" not in data:
        data["seriler"] = {}

    data["seriler"]["btc"] = {
        "ad": "Bitcoin",
        "birim": "USD",
        "seriKodu": "BTC-USD (Yahoo Finance)",
        "baslangic": min(yf_data["btc"].keys()) if yf_data["btc"] else None
    }
    data["seriler"]["bist100"] = {
        "ad": "Borsa İstanbul 100",
        "birim": "Endeks",
        "seriKodu": "XU100.IS (Yahoo Finance)",
        "baslangic": min(yf_data["bist100"].keys()) if yf_data["bist100"] else None
    }

    # Tabloyu güncelle
    veri_table = data.get("veri", {})
    all_dates = set(veri_table.keys()) | set(yf_data["btc"].keys()) | set(yf_data["bist100"].keys())

    for d in all_dates:
        if d not in veri_table:
            veri_table[d] = {
                "usd": None, "eur": None, "altin": None,
                "gumus": None, "benzin": None, "tufe": None
            }
        veri_table[d]["btc"] = yf_data["btc"].get(d)
        veri_table[d]["bist100"] = yf_data["bist100"].get(d)

    # Sırala ve kaydet
    sorted_veri = {k: veri_table[k] for k in sorted(veri_table.keys())}
    data["veri"] = sorted_veri

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(',', ':'))

    print(f"[OK] {JSON_PATH} basariyla BTC ve BIST100 ile guncellendi!")

if __name__ == "__main__":
    main()
