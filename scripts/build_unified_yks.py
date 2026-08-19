# -*- coding: utf-8 -*-
"""
acik-veri / scripts / build_unified_yks.py

YKS üniversite programlarını tek ve benzersiz (unique program code)
bir veri modelinde birleştirir.

Her program nesnesi:
- Sabit metaveriler (kod, üniversite, şehir, fakülte, bölüm, dil, burs vb.)
- latest: En güncel yılın özet verisi (kontenjan, taban puan, tavan puan, başarı sırası)
- history: Yıllara göre (2026, 2025, 2024, 2023, 2022) sıralı dizi
- rankTrend: Sıralama trendi ('up' | 'down' | 'flat')
- projectedRank: Tahmini başarı sırası

Çıktı Yolu:
  yks/programs_tyt.json
  yks/programs_say.json
  yks/programs_ea.json
  yks/programs_soz.json
  yks/programs_dil.json
  yks/departments.json
  yks/meta.json
"""

import json
import os
from collections import defaultdict

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rh_path = r"C:\Users\HP\proje\devam_eden\ykstercihbotu\arsiv\rank_history.full.json"

print(f"Sıralama geçmişi okunuyor: {rh_path}")
with open(rh_path, "r", encoding="utf-8") as f:
    rank_history = json.load(f)

score_types = ["tyt", "say", "ea", "soz", "dil"]
yks_out_dir = os.path.join(root_dir, "yks")
os.makedirs(yks_out_dir, exist_ok=True)

all_universities = set()
all_cities = set()
dept_map = defaultdict(lambda: {
    "name": "",
    "count": 0,
    "scoreTypes": set(),
    "faculties": set(),
    "minMin": float("inf"),
    "maxMax": float("-inf"),
    "bestRank": float("inf"),
    "history": defaultdict(list)
})

total_all_programs = 0
counts_summary = {}

print("\n--- BİRLEŞİK YKS PROGRAM VERİLERİ ÜRETİLİYOR ---")

for st in score_types:
    fname = f"programs_{st}.json"
    f25_path = os.path.join(root_dir, "yks", "2025", fname)
    f26_path = os.path.join(root_dir, "yks", "2026", fname)
    
    p_map = {}
    
    # 1. 2025 verilerini yükle
    if os.path.exists(f25_path):
        with open(f25_path, "r", encoding="utf-8") as f:
            for p in json.load(f):
                code = str(p["code"]).strip()
                p_map[code] = {
                    "code": code,
                    "univType": p.get("univType"),
                    "university": p.get("university"),
                    "city": p.get("city"),
                    "faculty": p.get("faculty"),
                    "program": p.get("program"),
                    "scoreType": p.get("scoreType"),
                    "scholarship": p.get("scholarship", "none"),
                    "language": p.get("language", "tr"),
                    "eduType": p.get("eduType", "formal"),
                    "history": {}
                }
                p_map[code]["history"][2025] = {
                    "quota": p.get("quota"),
                    "placed": p.get("placed"),
                    "minScore": p.get("minScore"),
                    "maxScore": p.get("maxScore"),
                    "minRank": p.get("minRank")
                }

    # 2. 2026 verilerini yükle ve güncelle
    if os.path.exists(f26_path):
        with open(f26_path, "r", encoding="utf-8") as f:
            for p in json.load(f):
                code = str(p["code"]).strip()
                if code not in p_map:
                    p_map[code] = {
                        "code": code,
                        "univType": p.get("univType"),
                        "university": p.get("university"),
                        "city": p.get("city"),
                        "faculty": p.get("faculty"),
                        "program": p.get("program"),
                        "scoreType": p.get("scoreType"),
                        "scholarship": p.get("scholarship", "none"),
                        "language": p.get("language", "tr"),
                        "eduType": p.get("eduType", "formal"),
                        "history": {}
                    }
                else:
                    if p.get("university"): p_map[code]["university"] = p["university"]
                    if p.get("program"): p_map[code]["program"] = p["program"]
                    if p.get("faculty"): p_map[code]["faculty"] = p["faculty"]
                    if p.get("city"): p_map[code]["city"] = p["city"]

                p_map[code]["history"][2026] = {
                    "quota": p.get("quota"),
                    "placed": p.get("placed"),
                    "minScore": p.get("minScore"),
                    "maxScore": p.get("maxScore"),
                    "minRank": p.get("minRank")
                }

    # 3. rank_history'den geçmiş yılları (2022, 2023, 2024) bağla
    for code, item in p_map.items():
        rh_item = rank_history.get(code)
        if rh_item:
            item["rankTrend"] = rh_item.get("rankTrend", "flat")
            item["projectedRank"] = rh_item.get("projectedRank")
            y_data = rh_item.get("y", {})
            for yr_str, yr_val in y_data.items():
                try:
                    yr_int = int(yr_str)
                    if yr_int not in item["history"]:
                        item["history"][yr_int] = {
                            "quota": None,
                            "placed": None,
                            "minScore": yr_val.get("taban"),
                            "maxScore": None,
                            "minRank": yr_val.get("sira")
                        }
                    else:
                        if not item["history"][yr_int].get("minRank"):
                            item["history"][yr_int]["minRank"] = yr_val.get("sira")
                except:
                    pass
        else:
            item["rankTrend"] = None
            item["projectedRank"] = None

        # history'yi sıralı diziye dönüştür
        hist_list = []
        for y_num in sorted(item["history"].keys(), reverse=True):
            h_data = item["history"][y_num]
            h_data["year"] = y_num
            hist_list.append(h_data)

        item["history"] = hist_list
        item["latest"] = hist_list[0] if hist_list else None

        # İstatistikler
        if item.get("university"):
            all_universities.add(item["university"])
        if item.get("city"):
            all_cities.add(item["city"])

        prog_name = item.get("program", "")
        if prog_name:
            d = dept_map[prog_name]
            d["name"] = prog_name
            d["count"] += 1
            d["scoreTypes"].add(item.get("scoreType", st.upper()))
            if item.get("faculty"):
                d["faculties"].add(item["faculty"])
            if item.get("latest") and item["latest"].get("minScore"):
                d["minMin"] = min(d["minMin"], item["latest"]["minScore"])
            if item.get("latest") and item["latest"].get("maxScore"):
                d["maxMax"] = max(d["maxMax"], item["latest"]["maxScore"])
            if item.get("latest") and item["latest"].get("minRank"):
                d["bestRank"] = min(d["bestRank"], item["latest"]["minRank"])

    # 4. JSON dosyasını yaz
    unified_list = sorted(p_map.values(), key=lambda x: (x.get("university", ""), x.get("program", "")))
    out_file_path = os.path.join(yks_out_dir, fname)
    with open(out_file_path, "w", encoding="utf-8") as f:
        json.dump(unified_list, f, ensure_ascii=False, separators=(',', ':'))

    size_kb = os.path.getsize(out_file_path) / 1024
    counts_summary[st] = len(unified_list)
    total_all_programs += len(unified_list)
    print(f"  {fname:20s}: {len(unified_list):6d} benzersiz program | {size_kb:8.1f} KB")

# 5. departments.json üretimi
departments = []
for name, d in sorted(dept_map.items()):
    departments.append({
        "name": name,
        "count": d["count"],
        "scoreTypes": sorted(list(d["scoreTypes"])),
        "faculty": sorted(list(d["faculties"]))[0] if d["faculties"] else "",
        "minMin": round(d["minMin"], 2) if d["minMin"] != float("inf") else None,
        "maxMax": round(d["maxMax"], 2) if d["maxMax"] != float("-inf") else None,
        "bestRank": d["bestRank"] if d["bestRank"] != float("inf") else None
    })

dept_path = os.path.join(yks_out_dir, "departments.json")
with open(dept_path, "w", encoding="utf-8") as f:
    json.dump(departments, f, ensure_ascii=False, separators=(',', ':'))
print(f"  {'departments.json':20s}: {len(departments):6d} benzersiz bölüm   | {os.path.getsize(dept_path)/1024:8.1f} KB")

# 6. meta.json üretimi
meta = {
    "name": "YKS Merkezi Yerleştirme Birleşik Veri Seti",
    "updatedAt": "2026-08-19",
    "yearsIncluded": [2022, 2023, 2024, 2025, 2026],
    "latestYear": 2026,
    "counts": counts_summary,
    "totalUniquePrograms": total_all_programs,
    "totalDepartments": len(departments),
    "universities": sorted(list(all_universities)),
    "cities": sorted(list(all_cities))
}

meta_path = os.path.join(yks_out_dir, "meta.json")
with open(meta_path, "w", encoding="utf-8") as f:
    json.dump(meta, f, ensure_ascii=False, separators=(',', ':'))
print(f"  {'meta.json':20s}: {len(meta['universities']):4d} üniversite, {len(meta['cities']):2d} şehir")

print(f"\n[BAŞARILI] Toplam {total_all_programs} benzersiz program tek bir dinamik havuzda birleştirildi!")
