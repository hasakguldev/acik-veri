import json
import os
import re

BASE_DIR = r"C:\Users\HP\proje\planlanan\sitematik\sitem\public\eglence"

def load_json(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict) and "response" in data:
        return json.loads(data["response"])
    return data

def save_json(filepath, data):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def merge_and_validate_all():
    print("=== EĞLENCE VERİLERİ BİRLEŞTİRME VE DOĞRULAMA MOTORU ===\n")
    
    # 1. SAYAÇLAR
    p_sayac1 = os.path.join(BASE_DIR, "sayaclar.json")
    p_sayac2 = os.path.join(BASE_DIR, "sayaclar3.json")
    d1_sayac = load_json(p_sayac1)
    d2_sayac = load_json(p_sayac2)
    
    k1_sayac = d1_sayac.get("kayitlar", [])
    k2_sayac = d2_sayac.get("kayitlar", [])
    
    alias_map = {
        "asgari-ucret-mesai-kazanci": "asgari-ucret-mesai-kazanc",
        "kidem-tazminati-tavan-birikimi": "kidem-tazminati-tavan-birikim",
        "turkiye-kartli-odeme-cirosu": "kartli-odeme-hacmi-turkiye",
        "turkiye-elektrik-tuketimi": "elektrik-ulusal-tuketim",
        "turkiye-motorin-tuketimi": "motorin-ulusal-tuketim-hacmi",
        "turkiye-benzin-tuketimi": "benzin-ulusal-tuketim-hacmi",
        "turkiye-cay-tuketimi": "cay-ulusal-tuketim-bardak",
        "turkiye-ekmek-tuketimi": "ekmek-ulusal-uretim",
        "turkiye-yeni-dogan-bebek": "dogum-sayisi-turkiye",
        "kadin-emeklilik-yas-sayaci": "emeklilik-kadin-yas-hedefi",
        "erkek-emeklilik-yas-sayaci": "emeklilik-erkek-yas-hedefi",
        "emeklilik-prim-gun-sayaci": "emeklilik-prim-gun-hedefi",
        "standart-otomobil-mtv-payi": "mtv-binek-arac-yuku",
        "standart-kdv-akisi": "kdv-alisveris-sepeti-payi",
        "turkiye-kargo-teslimati": "kargo-dagitim-sureci-maliyeti",
        "taksi-seyir-ucreti": "taksi-akici-yolculuk-tutari",
        "standart-mesken-dogalgaz-maliyeti": "dogalgaz-konut-tuketim-bedeli",
        "sigara-tiryakisi-harcama": "sigara-gunluk-paket-maliyeti",
    }
    
    sayac_merged = {}
    for item in k1_sayac:
        key = item["anahtar"].strip()
        canonical_key = alias_map.get(key, key)
        item["anahtar"] = canonical_key
        # Varsayılan değerler
        item.setdefault("hassasiyet", 2)
        item.setdefault("yon", "artan")
        sayac_merged[canonical_key] = item
        
    for item in k2_sayac:
        key = item["anahtar"].strip()
        canonical_key = alias_map.get(key, key)
        item["anahtar"] = canonical_key
        item.setdefault("hassasiyet", 2)
        item.setdefault("yon", "artan")
        
        if canonical_key in sayac_merged:
            existing = sayac_merged[canonical_key]
            # Açıklama veya başlık sayaclar3'te daha zenginse
            for f in ["baslik", "aciklama", "birim", "ikon", "parametre", "periyot", "yon", "hassasiyet"]:
                if f in item and item[f] is not None:
                    if f == "ikon" and item[f].startswith("fas fa-"):
                        existing[f] = item[f]
                    elif f == "parametre" and existing.get(f) is None:
                        existing[f] = item[f]
        else:
            sayac_merged[canonical_key] = item
            
    final_sayaclar = {
        "surum": "1.0.0",
        "kayitlar": list(sayac_merged.values())
    }
    save_json(p_sayac1, final_sayaclar)
    print(f"[OK] sayaclar.json guncellendi ({len(final_sayaclar['kayitlar'])} kayit).")

    # 2. SIRALAMA KIYAS
    p_kiyas1 = os.path.join(BASE_DIR, "siralama-kiyas.json")
    p_kiyas2 = os.path.join(BASE_DIR, "siralama-kiyas2.json")
    d1_kiyas = load_json(p_kiyas1)
    d2_kiyas = load_json(p_kiyas2)
    
    k1_kiyas = d1_kiyas.get("kayitlar", [])
    k2_kiyas = d2_kiyas.get("kayitlar", [])
    
    kiyas_merged = {}
    valid_turlar = {
        "stadyum", "ilce", "ilkokul", "universite", "ucak", "gemi",
        "konser", "koy", "mahalle", "hastane", "meslek", "sehir",
        "ada", "toplu-tasima", "festival", "ordu", "sirket"
    }
    
    for item in k1_kiyas:
        key = (item["tur"].strip().lower(), item["ad"].strip().lower())
        if item["tur"] not in valid_turlar:
            print(f"Uyari: Gecersiz tur '{item['tur']}' -> {item['ad']}")
        item["sayi"] = int(item["sayi"])
        item["birim"] = "kişi"
        kiyas_merged[key] = item
        
    for item in k2_kiyas:
        key = (item["tur"].strip().lower(), item["ad"].strip().lower())
        if item["tur"] not in valid_turlar:
            print(f"Uyari: Gecersiz tur '{item['tur']}' -> {item['ad']}")
        item["sayi"] = int(item["sayi"])
        item["birim"] = "kişi"
        if key in kiyas_merged:
            existing = kiyas_merged[key]
            for f in ["sayi", "birim", "sehir", "kalip", "kaynak"]:
                if existing.get(f) is None and item.get(f) is not None:
                    existing[f] = item[f]
        else:
            kiyas_merged[key] = item
            
    kiyas_kayitlar = list(kiyas_merged.values())
    kiyas_kayitlar.sort(key=lambda x: x.get("sayi", 0))
    
    final_kiyas = {
        "surum": "1.0.0",
        "guncelleme": "2026-08-21",
        "kayitlar": kiyas_kayitlar
    }
    save_json(p_kiyas1, final_kiyas)
    print(f"[OK] siralama-kiyas.json guncellendi ({len(final_kiyas['kayitlar'])} kayit).")

    # 3. FİYAT KALEMLERİ
    p_fiyat1 = os.path.join(BASE_DIR, "fiyat-kalemleri.json")
    p_fiyat2 = os.path.join(BASE_DIR, "fiyat-kalemleri2.json")
    d1_fiyat = load_json(p_fiyat1)
    d2_fiyat = load_json(p_fiyat2)
    
    k1_fiyat = d1_fiyat.get("kayitlar", [])
    k2_fiyat = d2_fiyat.get("kayitlar", [])
    
    valid_kategoriler = {
        "akaryakit", "gida", "ulasim", "vergi-harc", "resmi-ucret", "saglik",
        "egitim", "konut", "iletisim", "eglence", "kargo", "hizmet"
    }
    
    fiyat_merged = {}
    for item in k1_fiyat:
        key = item["ad"].strip().lower()
        if item["kategori"] not in valid_kategoriler:
            print(f"Uyari: Gecersiz kategori '{item['kategori']}' -> {item['ad']}")
        item["fiyat"] = None
        fiyat_merged[key] = item
        
    for item in k2_fiyat:
        key = item["ad"].strip().lower()
        if item["kategori"] not in valid_kategoriler:
            print(f"Uyari: Gecersiz kategori '{item['kategori']}' -> {item['ad']}")
        item["fiyat"] = None
        if key in fiyat_merged:
            existing = fiyat_merged[key]
            for f in ["kategori", "birim", "ikon", "fiyatKaynagi"]:
                if existing.get(f) is None and item.get(f) is not None:
                    existing[f] = item[f]
        else:
            fiyat_merged[key] = item
            
    fiyat_kayitlar = list(fiyat_merged.values())
    fiyat_kayitlar.sort(key=lambda x: (x.get("kategori", ""), x.get("ad", "")))
    
    final_fiyat = {
        "surum": "1.0.0",
        "kayitlar": fiyat_kayitlar
    }
    save_json(p_fiyat1, final_fiyat)
    print(f"[OK] fiyat-kalemleri.json guncellendi ({len(final_fiyat['kayitlar'])} kayit).")

if __name__ == "__main__":
    merge_and_validate_all()
