# -*- coding: utf-8 -*-
"""
Türkiye il / ilçe / mahalle (köy) veri seti üreticisi
=====================================================

Kaynak: PTT A.Ş. posta kodu listesi (https://postakodu.ptt.gov.tr, `pk_list.zip`).
Sütunlar: il, ilçe, semt_bucak_belde, Mahalle, PK.

İki girdi biçimi kabul edilir:
    --ptt  <pk_list.zip | pk_list.xlsx>      PTT'nin resmî dosyası (openpyxl gerekir)
    --json <neighbourhoods.json>             turkey-neighbourhoods (MIT) paketinin aynı
                                             PTT listesinden ürettiği satırlar:
                                             [plaka, il, ilçe, mahalle, posta kodu]

Çıktı (`adres/`):
    meta.json                 kaynak, tarih, sayılar, kimlik kuralı
    iller.json                [{kod, ad, ilceSayisi, mahalleSayisi}]
    ilceler.json              {"34": [{id, ad, mahalleSayisi}], ...}
    mahalleler/<plaka>.json   bir ilin tüm ilçe ve mahalleleri (satırlar dizi)
    tum.json                  bütün ülke tek dosyada, aynı satır biçimiyle

Kimlikler kararlıdır ve adlardan türetilir (Türkçe karakterler sadeleştirilir):
    il      "34"                         plaka kodu
    ilçe    "34-kartal"                  plaka + ilçe
    mahalle "34-kartal-atalar"           ilçe + mahalle
            "34-...-akdurak-koyu"        köyler "-koyu" ekiyle
            "...-cakmak-akdurak-koyu"    bir köye/beldeye bağlı mahalleler bağlı yerle
Aynı ilçede kimlik çakışırsa posta kodu eklenir. Tüketiciler bölge seçimlerini bu
kimliklerle saklar; ad değişikliği kimliği de değiştirir, bu yüzden seçimle birlikte
adı da saklamaları önerilir.

Çalıştırma:
    python scripts/build_adres.py --ptt pk_list.zip
    python scripts/build_adres.py --json neighbourhoods.json --kaynak-tarihi 2024-03-31
"""

import argparse
import datetime as dt
import io
import json
import os
import re
import sys
import zipfile
from collections import OrderedDict, defaultdict

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CIKTI = os.path.join(KOK, "adres")
SATIR_ALANLARI = ["id", "ad", "tur", "pk"]

KUCUK = str.maketrans({"I": "ı", "İ": "i"})
BUYUK = str.maketrans({"i": "İ", "ı": "I"})
SADE = str.maketrans({"ç": "c", "ğ": "g", "ı": "i", "ö": "o", "ş": "s", "ü": "u", "â": "a", "î": "i", "û": "u"})


def kucult(metin):
    return metin.translate(KUCUK).lower()


def baslik(metin):
    """Türkçe başlık düzeni: her sözcüğün (parantez ve tire sonrası dahil) ilk harfi büyük."""
    metin = re.sub(r"\s+", " ", metin.strip())
    parcalar = re.split(r"([\s(\-/.])", kucult(metin))
    return "".join(p[:1].translate(BUYUK).upper() + p[1:] if p and p[0].isalpha() else p for p in parcalar)


def sade(metin):
    s = kucult(metin).translate(SADE)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


MAH = re.compile(r"^(?P<ad>.+?)\s+Mah\.?(?:allesi)?(?:\s*\((?P<bagli>.+)\))?$")
KOY = re.compile(r"^(?P<ad>.+?)\s+Köyü$")


def ayristir(ham):
    """PTT adını (ör. 'Çakmak Mah (Akdurak Köyü)') görünen ada, türe ve kimlik köküne çevirir."""
    ad = baslik(ham)
    m = MAH.match(ad)
    if m:
        bagli = m.group("bagli")
        gorunen = f"{m.group('ad')} Mahallesi" + (f" ({bagli})" if bagli else "")
        kok = sade(m.group("ad")) + (f"-{sade(bagli)}" if bagli else "")
        return gorunen, "mahalle", kok
    k = KOY.match(ad)
    if k:
        return ad, "koy", sade(k.group("ad")) + "-koyu"
    return ad, "diger", sade(ad)


def turkce_harf(metin):
    return sum(1 for h in metin if h in "çğıöşüÇĞİÖŞÜ")


def ptt_oku(yol):
    try:
        import openpyxl  # noqa: WPS433 - yalnız PTT girdisinde gerekir
    except ImportError:
        sys.exit("PTT dosyası için openpyxl gerekir: pip install openpyxl")
    if yol.lower().endswith(".zip"):
        with zipfile.ZipFile(yol) as z:
            ad = next(n for n in z.namelist() if n.lower().endswith(".xlsx"))
            veri = io.BytesIO(z.read(ad))
    else:
        veri = yol
    sayfa = openpyxl.load_workbook(veri, read_only=True, data_only=True).worksheets[0]
    satirlar = sayfa.iter_rows(values_only=True)
    basliklar = [kucult(str(h or "")).strip() for h in next(satirlar)]

    def sutun(*adlar):
        for a in adlar:
            if a in basliklar:
                return basliklar.index(a)
        sys.exit(f"Beklenen sütun yok: {adlar} — bulunan: {basliklar}")

    i_il, i_ilce, i_mah, i_pk = sutun("il"), sutun("ilçe", "ilce"), sutun("mahalle"), sutun("pk", "posta kodu")
    for r in satirlar:
        if not r or not r[i_il]:
            continue
        pk = str(r[i_pk]).strip().zfill(5)
        yield pk[:2], str(r[i_il]), str(r[i_ilce]), str(r[i_mah]), pk


def json_oku(yol):
    with open(yol, encoding="utf-8") as f:
        for plaka, il, ilce, mah, pk in json.load(f):
            yield str(plaka).zfill(2), il, ilce, mah, str(pk).zfill(5)


def uret(kayitlar):
    iller = OrderedDict()
    for plaka, il, ilce, mah, pk in kayitlar:
        il_kaydi = iller.setdefault(plaka, {"kod": plaka, "ad": baslik(il), "ilceler": OrderedDict()})
        ilce_ad = baslik(ilce)
        ilce_id = f"{plaka}-{sade(ilce_ad)}"
        ilce_kaydi = il_kaydi["ilceler"].setdefault(ilce_id, {"id": ilce_id, "ad": ilce_ad, "mahalleler": []})
        ad, tur, kok = ayristir(mah)
        ilce_kaydi["mahalleler"].append({"kok": kok, "ad": ad, "tur": tur, "pk": pk})

    sayilar = {"il": 0, "ilce": 0, "mahalle": 0, "koy": 0, "diger": 0, "birlesen": 0}
    for il in iller.values():
        sayilar["il"] += 1
        for ilce in il["ilceler"].values():
            sayilar["ilce"] += 1
            # Aynı yer iki kez geçebilir: farklı semt altında aynı ad, ya da aynı posta
            # kodunda iki yazım (PTT'de "Cuhalar" / "Çuhalar"). Kimlik kökü ve posta kodu
            # aynıysa tek kayıt tutulur; Türkçe karakterli yazım yeğlenir.
            tekil = OrderedDict()
            for m in ilce["mahalleler"]:
                anahtar = (m["kok"], m["pk"])
                onceki = tekil.get(anahtar)
                if onceki is None:
                    tekil[anahtar] = m
                    continue
                if onceki["ad"] != m["ad"]:
                    sayilar["birlesen"] += 1
                    if turkce_harf(m["ad"]) > turkce_harf(onceki["ad"]):
                        tekil[anahtar] = m
            ayni_ad = OrderedDict()
            for m in tekil.values():
                ayni_ad.setdefault((m["kok"], m["ad"]), m)
            tekil = ayni_ad
            koke_gore = defaultdict(list)
            for m in tekil.values():
                koke_gore[m["kok"]].append(m)
            satirlar = []
            for m in tekil.values():
                kimlik = f"{ilce['id']}-{m['kok']}"
                if len(koke_gore[m["kok"]]) > 1:
                    kimlik += f"-{m['pk']}"
                satirlar.append([kimlik, m["ad"], m["tur"], m["pk"]])
                sayilar[m["tur"]] += 1
            satirlar.sort(key=lambda s: kucult(s[1]).translate(SADE))
            ilce["mahalleler"] = satirlar
        il["ilceler"] = sorted(il["ilceler"].values(), key=lambda i: kucult(i["ad"]).translate(SADE))
    return OrderedDict(sorted(iller.items())), sayilar


def denetle(iller):
    gorulen = set()
    for il in iller.values():
        for ilce in il["ilceler"]:
            if ilce["id"] in gorulen:
                sys.exit(f"Yinelenen ilçe kimliği: {ilce['id']}")
            gorulen.add(ilce["id"])
            for satir in ilce["mahalleler"]:
                if satir[0] in gorulen:
                    sys.exit(f"Yinelenen mahalle kimliği: {satir[0]}")
                gorulen.add(satir[0])


def yaz(ad, veri):
    yol = os.path.join(CIKTI, ad)
    os.makedirs(os.path.dirname(yol), exist_ok=True)
    with open(yol, "w", encoding="utf-8") as f:
        json.dump(veri, f, ensure_ascii=False, separators=(",", ":"))
        f.write("\n")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--ptt", help="PTT pk_list.zip veya .xlsx")
    g.add_argument("--json", help="turkey-neighbourhoods neighbourhoods.json")
    p.add_argument("--kaynak-tarihi", help="Kaynak listenin tarihi (YYYY-AA-GG); PTT için varsayılan bugündür")
    a = p.parse_args()

    kayitlar = ptt_oku(a.ptt) if a.ptt else json_oku(a.json)
    iller, sayilar = uret(kayitlar)
    denetle(iller)
    if sayilar["il"] != 81:
        sys.exit(f"81 il beklenirken {sayilar['il']} il bulundu; kaynak dosya eksik olabilir.")

    bugun = dt.date.today().isoformat()
    kaynak_tarihi = a.kaynak_tarihi or bugun
    for il in iller.values():
        yaz(f"mahalleler/{il['kod']}.json", {"il": {"kod": il["kod"], "ad": il["ad"]}, "alanlar": SATIR_ALANLARI, "ilceler": il["ilceler"]})
    yaz("tum.json", {"alanlar": SATIR_ALANLARI, "iller": list(iller.values())})
    yaz("iller.json", [
        {"kod": il["kod"], "ad": il["ad"], "ilceSayisi": len(il["ilceler"]), "mahalleSayisi": sum(len(i["mahalleler"]) for i in il["ilceler"])}
        for il in iller.values()
    ])
    yaz("ilceler.json", {
        il["kod"]: [{"id": i["id"], "ad": i["ad"], "mahalleSayisi": len(i["mahalleler"])} for i in il["ilceler"]]
        for il in iller.values()
    })
    meta = OrderedDict([
        ("name", "Türkiye İl, İlçe ve Mahalle (Köy) Listesi"),
        ("source", "PTT A.Ş. Posta Kodu Listesi"),
        ("sourceUrl", "https://postakodu.ptt.gov.tr"),
        ("sourceDate", kaynak_tarihi),
        ("generatedAt", bugun),
        ("via", "PTT dosyası" if a.ptt else "turkey-neighbourhoods (MIT, Murat Gözel) paketindeki PTT listesi"),
        ("counts", OrderedDict([("il", sayilar["il"]), ("ilce", sayilar["ilce"]), ("mahalle", sayilar["mahalle"]),
                                ("koy", sayilar["koy"]), ("diger", sayilar["diger"]),
                                ("toplam", sayilar["mahalle"] + sayilar["koy"] + sayilar["diger"]),
                                ("birlesenYazimFarki", sayilar["birlesen"])])),
        ("rowFields", SATIR_ALANLARI),
        ("types", {"mahalle": "Mahalle", "koy": "Köy", "diger": "Yayla, mezra vb. diğer yerleşim"}),
        ("idRule", "il: plaka; ilçe: <plaka>-<ilçe>; mahalle: <ilçe kimliği>-<ad>[-<bağlı köy/belde>]; köy: ...-<ad>-koyu; çakışmada -<posta kodu>"),
        ("files", ["meta.json", "iller.json", "ilceler.json", "mahalleler/<plaka>.json", "tum.json"]),
    ])
    yaz("meta.json", meta)
    manifesti_guncelle(meta)
    print(json.dumps(meta["counts"], ensure_ascii=False))


def manifesti_guncelle(meta):
    """manifest.json'daki adres kaydının sayı ve tarihini yeni veriyle eşitler."""
    yol = os.path.join(KOK, "manifest.json")
    with open(yol, encoding="utf-8") as f:
        manifest = json.load(f, object_pairs_hook=OrderedDict)
    kayit = manifest.get("datasets", {}).get("adres")
    if not kayit or (kayit.get("counts") == meta["counts"] and kayit.get("sourceDate") == meta["sourceDate"]):
        return
    kayit["counts"] = meta["counts"]
    kayit["sourceDate"] = meta["sourceDate"]
    manifest["updatedAt"] = meta["generatedAt"]
    with open(yol, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
        f.write("\n")


if __name__ == "__main__":
    main()
