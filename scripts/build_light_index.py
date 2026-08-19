# -*- coding: utf-8 -*-
"""
Hafif indeks üreticisi
======================

Tam veri setleri (yks/programs_*.json ~18 MB, lgs/schools.json ~1,5 MB) tarayıcıda
tek seferde indirilemeyecek kadar büyüktür. Bu betik, tercih/karşılaştırma
araçlarının ihtiyaç duyduğu asgari alanları sözlük kodlamasıyla (dictionary
encoding) sıkıştırılmış "hafif indeks" dosyalarına dönüştürür.

Biçim:
    {
      "year": 2026,
      "dicts": { "univ": [...], "city": [...], "program": [...] },
      "fields": ["code", "u", "c", "p", "sch", "lang", "minScore", "minRank", "quota"],
      "rows": [ ["106510077", 0, 0, 12, 0, 0, 443.23, 46890, 80], ... ]
    }

Sözlük alanları tamsayı indeks olarak saklanır; tekrar eden üniversite, şehir ve
program adları bir kez yazılır. Tipik kazanç: %75-85 boyut düşüşü.

Çalıştırma:
    python scripts/build_light_index.py
"""

import json
import os
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
CIKTI_YKS = KOK / "yks" / "light"
CIKTI_LGS = KOK / "lgs" / "light"

PUAN_TURLERI = ["say", "ea", "soz", "dil", "tyt"]
LGS_KATEGORILERI = ["fen", "anadolu", "imamhatip", "meslek", "sosyal"]


class Sozluk:
    """Tekrar eden metinleri tamsayı indekse çeviren sözlük."""

    def __init__(self):
        self.liste = []
        self.harita = {}

    def indeks(self, deger):
        if deger is None:
            return -1
        if deger not in self.harita:
            self.harita[deger] = len(self.liste)
            self.liste.append(deger)
        return self.harita[deger]


def yuvarla(x, basamak=2):
    return None if x is None else round(float(x), basamak)


def yaz(yol: Path, veri):
    yol.parent.mkdir(parents=True, exist_ok=True)
    with open(yol, "w", encoding="utf-8") as f:
        json.dump(veri, f, ensure_ascii=False, separators=(",", ":"))
    return yol.stat().st_size


# --------------------------------------------------------------------- YKS ---

def yks_indeksi(puan_turu: str):
    kaynak = KOK / "yks" / f"programs_{puan_turu}.json"
    if not kaynak.exists():
        print(f"  ! {kaynak.name} bulunamadı, atlanıyor")
        return None

    with open(kaynak, encoding="utf-8") as f:
        programlar = json.load(f)
    if isinstance(programlar, dict):
        programlar = programlar.get("programs", [])

    d_univ, d_city, d_prog, d_fac = Sozluk(), Sozluk(), Sozluk(), Sozluk()
    satirlar = []
    yil = None

    for p in programlar:
        gecmis = p.get("history") or []
        son = p.get("latest") or (gecmis[0] if gecmis else {})
        if yil is None:
            yil = son.get("year")

        # Bir önceki yılın taban puanı — trend göstermek için
        onceki = None
        for h in gecmis[1:]:
            if h.get("minScore") is not None:
                onceki = h
                break

        satirlar.append([
            p.get("code"),
            d_univ.indeks(p.get("university")),
            d_city.indeks(p.get("city")),
            d_prog.indeks(p.get("program")),
            d_fac.indeks(p.get("faculty")),
            p.get("scholarship") or "none",
            p.get("language") or "tr",
            p.get("eduType") or "formal",
            0 if p.get("univType") == "DEVLET" else (1 if p.get("univType") == "VAKIF" else 2),
            yuvarla(son.get("minScore"), 3),
            son.get("minRank"),
            son.get("quota"),
            yuvarla(onceki.get("minScore"), 3) if onceki else None,
            onceki.get("minRank") if onceki else None,
        ])

    veri = {
        "scoreType": puan_turu.upper(),
        "year": yil,
        "count": len(satirlar),
        "dicts": {
            "univ": d_univ.liste,
            "city": d_city.liste,
            "program": d_prog.liste,
            "faculty": d_fac.liste,
        },
        "fields": [
            "code", "u", "c", "p", "f", "sch", "lang", "edu", "type",
            "minScore", "minRank", "quota", "prevScore", "prevRank",
        ],
        "rows": satirlar,
    }

    hedef = CIKTI_YKS / f"{puan_turu}.json"
    boyut = yaz(hedef, veri)
    kaynak_boyut = kaynak.stat().st_size
    print(f"  yks/light/{puan_turu}.json  {len(satirlar):>6} program  "
          f"{kaynak_boyut/1048576:>6.2f} MB → {boyut/1048576:>5.2f} MB  "
          f"(%{100 - boyut*100/kaynak_boyut:.0f} küçüldü)")
    return {"file": f"light/{puan_turu}.json", "count": len(satirlar), "bytes": boyut}


# --------------------------------------------------------------------- LGS ---

def lgs_indeksi():
    kaynak = KOK / "lgs" / "schools.json"
    if not kaynak.exists():
        print("  ! lgs/schools.json bulunamadı, atlanıyor")
        return None

    with open(kaynak, encoding="utf-8") as f:
        okullar = json.load(f)
    if isinstance(okullar, dict):
        okullar = okullar.get("schools", [])

    d_city, d_dist, d_school, d_type, d_field = Sozluk(), Sozluk(), Sozluk(), Sozluk(), Sozluk()
    satirlar = []
    for o in okullar:
        satirlar.append([
            o.get("code"),
            d_city.indeks(o.get("city")),
            d_dist.indeks(o.get("district")),
            d_school.indeks(o.get("school")),
            d_type.indeks(o.get("schoolType")),
            d_field.indeks(o.get("field")),
            o.get("category"),
            yuvarla(o.get("minScore"), 3),
            o.get("emptyQuota"),
            o.get("language"),
            o.get("boarding"),
        ])

    veri = {
        "year": 2026,
        "count": len(satirlar),
        "dicts": {
            "city": d_city.liste, "district": d_dist.liste,
            "school": d_school.liste, "type": d_type.liste, "field": d_field.liste,
        },
        "fields": ["code", "c", "d", "s", "t", "f", "cat", "minScore", "quota", "lang", "boarding"],
        "rows": satirlar,
    }
    hedef = CIKTI_LGS / "schools.json"
    boyut = yaz(hedef, veri)
    kaynak_boyut = kaynak.stat().st_size
    print(f"  lgs/light/schools.json    {len(satirlar):>6} lise     "
          f"{kaynak_boyut/1048576:>6.2f} MB → {boyut/1048576:>5.2f} MB  "
          f"(%{100 - boyut*100/kaynak_boyut:.0f} küçüldü)")
    return {"file": "light/schools.json", "count": len(satirlar), "bytes": boyut}


def lgs_yetenek_indeksi():
    kaynak = KOK / "lgs" / "yetenek_okullari.json"
    if not kaynak.exists():
        print("  ! lgs/yetenek_okullari.json bulunamadı, atlanıyor")
        return None

    with open(kaynak, encoding="utf-8") as f:
        kayitlar = json.load(f)
    if isinstance(kayitlar, dict):
        kayitlar = kayitlar.get("schools", kayitlar.get("data", []))

    d_city, d_dist, d_school, d_field = Sozluk(), Sozluk(), Sozluk(), Sozluk()
    satirlar = []
    for k in kayitlar:
        satirlar.append([
            d_city.indeks(k.get("city")),
            d_dist.indeks(k.get("district")),
            d_school.indeks(k.get("school")),
            k.get("typeKey"),
            d_field.indeks(k.get("field")),
            k.get("quota"),
            k.get("quotaMale"),
            k.get("quotaFemale"),
        ])

    veri = {
        "year": 2026,
        "count": len(satirlar),
        "dicts": {"city": d_city.liste, "district": d_dist.liste,
                  "school": d_school.liste, "field": d_field.liste},
        "fields": ["c", "d", "s", "typeKey", "f", "quota", "quotaMale", "quotaFemale"],
        "rows": satirlar,
    }
    hedef = CIKTI_LGS / "yetenek.json"
    boyut = yaz(hedef, veri)
    kaynak_boyut = kaynak.stat().st_size
    print(f"  lgs/light/yetenek.json    {len(satirlar):>6} program  "
          f"{kaynak_boyut/1048576:>6.2f} MB → {boyut/1048576:>5.2f} MB  "
          f"(%{100 - boyut*100/kaynak_boyut:.0f} küçüldü)")
    return {"file": "light/yetenek.json", "count": len(satirlar), "bytes": boyut}


# --------------------------------------------------------------------- main --

def main():
    print("Hafif indeks üretimi\n" + "-" * 66)

    yks_ozet = {}
    for t in PUAN_TURLERI:
        sonuc = yks_indeksi(t)
        if sonuc:
            yks_ozet[t.upper()] = sonuc

    lgs_ozet = {}
    r = lgs_indeksi()
    if r:
        lgs_ozet["schools"] = r
    r = lgs_yetenek_indeksi()
    if r:
        lgs_ozet["yetenek"] = r

    # light/index.json — istemcinin ne indireceğini bilmesi için katalog
    if yks_ozet:
        yaz(CIKTI_YKS / "index.json", {
            "format": "dict-encoded-rows",
            "description": "Tercih araçları için sıkıştırılmış YKS program indeksi",
            "datasets": yks_ozet,
        })
    if lgs_ozet:
        yaz(CIKTI_LGS / "index.json", {
            "format": "dict-encoded-rows",
            "description": "Tercih araçları için sıkıştırılmış LGS okul indeksi",
            "datasets": lgs_ozet,
        })

    toplam = sum(v["bytes"] for v in list(yks_ozet.values()) + list(lgs_ozet.values()))
    print("-" * 66)
    print(f"Toplam hafif indeks boyutu: {toplam/1048576:.2f} MB")


if __name__ == "__main__":
    main()
