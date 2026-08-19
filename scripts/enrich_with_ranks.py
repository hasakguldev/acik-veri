# -*- coding: utf-8 -*-
"""
acik-veri / scripts / enrich_with_ranks.py

programs_*.json dosyalarına rank_history.full.json üzerinden:
- minRank (en son bilinen başarı sırası)
- projectedRank (tahmini başarı sırası)
- rankTrend ('up' | 'down' | 'flat')
- ranks ({ '2022': ..., '2023': ..., '2024': ... })

alanlarını ekleyerek veriyi zenginleştirir.
"""

import json
import os

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rh_path = r"C:\Users\HP\proje\devam_eden\ykstercihbotu\arsiv\rank_history.full.json"

print(f"Sıralama verisi okunuyor: {rh_path}")
with open(rh_path, "r", encoding="utf-8") as f:
    rank_history = json.load(f)

score_files = [
    "programs_tyt.json",
    "programs_say.json",
    "programs_ea.json",
    "programs_soz.json",
    "programs_dil.json"
]

years = ["2025", "2026"]

for y in years:
    ydir = os.path.join(root_dir, "yks", y)
    if not os.path.exists(ydir):
        continue
    
    print(f"\n--- [{y}] Programlar Sıralama Verisiyle Zenginleştiriliyor ---")
    total_matched = 0
    total_prog = 0

    for sfile in score_files:
        fpath = os.path.join(ydir, sfile)
        if not os.path.exists(fpath):
            continue

        with open(fpath, "r", encoding="utf-8") as f:
            programs = json.load(f)

        for p in programs:
            code = str(p.get("code", "")).strip()
            total_prog += 1
            if code in rank_history:
                total_matched += 1
                rh_item = rank_history[code]
                
                # Yıllara göre sıralamaları çıkar
                y_data = rh_item.get("y", {})
                ranks = {}
                latest_rank = None
                for yr in sorted(y_data.keys()):
                    sira_val = y_data[yr].get("sira")
                    if sira_val is not None and str(sira_val) not in ("--", "---", "", "None"):
                        try:
                            ranks[yr] = int(sira_val)
                            latest_rank = int(sira_val)
                        except (ValueError, TypeError):
                            pass

                p["minRank"] = latest_rank
                p["projectedRank"] = rh_item.get("projectedRank")
                p["rankTrend"] = rh_item.get("rankTrend", "flat")
                p["ranks"] = ranks
            else:
                p["minRank"] = None
                p["projectedRank"] = None
                p["rankTrend"] = None
                p["ranks"] = {}

        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(programs, f, ensure_ascii=False, separators=(',', ':'))

        size_kb = os.path.getsize(fpath) / 1024
        print(f"  {sfile:20s}: {len(programs):6d} program | {size_kb:8.1f} KB")

    print(f"  [OK] [{y}] Toplam: {total_prog}, Sıralaması eşleşen: {total_matched} (%{total_matched/total_prog*100:.1f})")

print("\n[TAMAMLANDI] Tüm YKS dosyaları sıralama (başarı sırası) verileriyle güncellendi.")
