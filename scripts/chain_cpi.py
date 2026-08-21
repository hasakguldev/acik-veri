import requests
import json
import pandas as pd

api_key = 'iTdDzQ48UM'
base_url = 'https://evds3.tcmb.gov.tr/igmevdsms-dis/'
headers = {'key': api_key}

def get_series(code, start="01-01-1980", end="01-08-2026"):
    url = f"{base_url}series={code}&startDate={start}&endDate={end}&type=json&frequency=5&aggregationTypes=avg"
    r = requests.get(url, headers=headers)
    items = r.json().get("items", [])
    key_f = code.replace(".", "_")
    res = {}
    for it in items:
        t = it.get("Tarih")
        if not t: continue
        parts = t.split("-")
        if len(parts) == 2:
            d_key = f"{int(parts[0]):04d}-{int(parts[1]):02d}"
        elif len(parts) == 3:
            d_key = f"{int(parts[0]):04d}-{int(parts[1]):02d}" if len(parts[0]) == 4 else f"{int(parts[2]):04d}-{int(parts[1]):02d}"
        else:
            continue
        v = it.get(key_f)
        if v is not None and str(v).strip() != "":
            try:
                res[d_key] = float(str(v).replace(",", "."))
            except:
                pass
    return res

print("=== TÜFE SERİLERİ ANALİZİ VE ZİNCİRLEME ===")
tufe_2003 = get_series("TP.FG.J0")       # 2003=100
tufe_1994 = get_series("TP.FG.T01")      # 1994=100
tufe_1987 = get_series("TP.FG.A01")      # 1987=100
tufe_1982 = get_series("TP.FG.F01")      # 1982=100
tufe_2025 = get_series("TP.FE25.OKTG01")  # 2025/2026 güncel

print(f"tufe_2003 (2003=100): {min(tufe_2003.keys())} -> {max(tufe_2003.keys())} ({len(tufe_2003)} ay)")
print(f"tufe_1994 (1994=100): {min(tufe_1994.keys())} -> {max(tufe_1994.keys())} ({len(tufe_1994)} ay)")
print(f"tufe_1987 (1987=100): {min(tufe_1987.keys())} -> {max(tufe_1987.keys())} ({len(tufe_1987)} ay)")
print(f"tufe_1982 (1982=100): {min(tufe_1982.keys())} -> {max(tufe_1982.keys())} ({len(tufe_1982)} ay)")
print(f"tufe_2025 (güncel):   {min(tufe_2025.keys())} -> {max(tufe_2025.keys())} ({len(tufe_2025)} ay)")

# 2003-2004 örtüşme oranı (1994=100 -> 2003=100)
# 2003 yılı ortalaması 2003=100'de tam 100'dür (veya ~100)
overlap_2003 = [k for k in sorted(tufe_2003.keys()) if k in tufe_1994 and k.startswith("2003")]
print(f"\n2003 Yılı Örtüşen Aylar (1994 vs 2003): {len(overlap_2003)}")
ratios_94_03 = [tufe_2003[k] / tufe_1994[k] for k in overlap_2003]
avg_ratio_94_03 = sum(ratios_94_03) / len(ratios_94_03)
print(f"1994=100 -> 2003=100 Zincirleme Çarpanı (2003 Ortalaması): {avg_ratio_94_03:.10f}")

# 1994 yılı örtüşme oranı (1987=100 -> 1994=100) veya 1987 -> 2003
overlap_87_94 = [k for k in sorted(tufe_1994.keys()) if k in tufe_1987 and k.startswith("1994")]
print(f"\n1994 Yılı Örtüşen Aylar (1987 vs 1994): {len(overlap_87_94)}")
ratios_87_94 = [tufe_1994[k] / tufe_1987[k] for k in overlap_87_94]
avg_ratio_87_94 = sum(ratios_87_94) / len(ratios_87_94)
print(f"1987=100 -> 1994=100 Zincirleme Çarpanı: {avg_ratio_87_94:.10f}")

# 1987 yılı örtüşme oranı (1982=100 -> 1987=100)
overlap_82_87 = [k for k in sorted(tufe_1987.keys()) if k in tufe_1982 and k.startswith("1987")]
print(f"\n1987 Yılı Örtüşen Aylar (1982 vs 1987): {len(overlap_82_87)}")
ratios_82_87 = [tufe_1987[k] / tufe_1982[k] for k in overlap_82_87]
avg_ratio_82_87 = sum(ratios_82_87) / len(ratios_82_87)
print(f"1982=100 -> 1987=100 Zincirleme Çarpanı: {avg_ratio_82_87:.10f}")

# Güncel TÜFE (2026-01 -> 2026-07)
# tufe_2025 ile tufe_2003 ilişkisi
overlap_curr = [k for k in sorted(tufe_2003.keys()) if k in tufe_2025 and k >= "2025-01"]
print(f"\n2025-2026 Örtüşen Aylar (2003 vs 2025): {overlap_curr}")
for k in overlap_curr:
    print(f"  {k}: tufe_2003={tufe_2003[k]}, tufe_2025={tufe_2025[k]}, Oran={tufe_2003[k]/tufe_2025[k]:.4f}")
