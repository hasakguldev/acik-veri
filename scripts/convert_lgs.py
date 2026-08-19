# -*- coding: utf-8 -*-
"""
acik-veri / scripts / convert_lgs.py

MEB LGS Merkezi Sınav Taban Puanları Excel tablosunu
standart ve modüler JSON formatına dönüştürür.

Çıktı Yolları:
  lgs/schools.json           (Tüm okullar)
  lgs/schools_fen.json       (Fen Liseleri)
  lgs/schools_anadolu.json   (Anadolu Liseleri)
  lgs/schools_imamhatip.json (Anadolu İmam Hatip Liseleri)
  lgs/schools_meslek.json    (Mesleki ve Teknik Liseler)
  lgs/schools_sosyal.json    (Sosyal Bilimler Liseleri)
  lgs/departments.json       (Alan/Program İstatistikleri)
  lgs/meta.json              (81 İl, İlçeler ve Genel Özet)
  lgs/index.json             (Şema Kılavuzu)
"""

import json
import os
import re
import sys
from collections import defaultdict
import pandas as pd

LANG_MAP = {
    'İngilizce': 'en',
    'Almanca': 'de',
    'Fransızca': 'fr',
    'İtalyanca': 'it',
    'İspanyolca': 'es',
    'Arapça': 'ar',
    'Rusça': 'ru',
    'Çince': 'zh',
    'Japonca': 'ja'
}

def parse_school_name(raw_name):
    """'ADANA / KOZAN / Fatih Anadolu Lisesi' -> ('ADANA', 'KOZAN', 'Fatih Anadolu Lisesi')"""
    if pd.isna(raw_name):
        return None, None, ""
    
    parts = [p.strip() for p in str(raw_name).split('/')]
    if len(parts) >= 3:
        city = parts[0]
        district = parts[1]
        school = '/'.join(parts[2:]).strip()
        return city, district, school
    elif len(parts) == 2:
        return parts[0], None, parts[1]
    return None, None, str(raw_name).strip()

def clean_score(val):
    if pd.isna(val):
        return None
    s = str(val).strip().replace(',', '.')
    if s in ('--', '---', '', 'nan', 'None'):
        return None
    try:
        f = float(s)
        return round(f, 4)
    except ValueError:
        return None

def categorize_school_type(type_str):
    t = str(type_str).lower().replace('i̇', 'i').replace('ı', 'i').replace('ö', 'o').replace('ü', 'u').replace('ş', 's').replace('ç', 'c').replace('ğ', 'g')
    if 'fen' in t:
        return 'fen'
    elif 'imam' in t or 'hatip' in t:
        return 'imamhatip'
    elif 'meslek' in t or 'teknik' in t:
        return 'meslek'
    elif 'sosyal' in t:
        return 'sosyal'
    elif 'anadolu' in t:
        return 'anadolu'
    return 'diger'

def convert_lgs(excel_path, out_base_dir):
    lgs_dir = os.path.join(out_base_dir, 'lgs')
    os.makedirs(lgs_dir, exist_ok=True)

    print(f"LGS Excel dosyası okunuyor: {excel_path}")
    df = pd.read_excel(excel_path, header=101)

    all_schools = []
    by_category = {
        'fen': [],
        'anadolu': [],
        'imamhatip': [],
        'meslek': [],
        'sosyal': [],
        'diger': []
    }

    cities = set()
    districts_by_city = defaultdict(set)
    fields_map = defaultdict(lambda: {
        'count': 0,
        'schoolTypes': set(),
        'minMin': float('inf'),
        'maxMax': float('-inf')
    })

    for _, row in df.iterrows():
        code_raw = row.get('Tercih Kodu')
        if pd.isna(code_raw):
            continue
        try:
            code = str(int(float(str(code_raw).strip())))
        except (ValueError, TypeError):
            code = str(code_raw).strip()

        raw_school_name = row.get('Okul Adı')
        city, district, school_name = parse_school_name(raw_school_name)
        if not school_name:
            continue

        school_type = str(row.get('Okul Türü', '')).strip()
        field_name = str(row.get('Alan Adı', '')).strip() if pd.notna(row.get('Alan Adı')) else None
        duration = str(row.get('Öğretim Süresi', '4 yıl')).strip()
        gender = str(row.get('Öğretim Şekli', 'Kız/Erkek')).strip()
        boarding = str(row.get('Pansiyon Durumu', 'Yok')).strip()
        lang_raw = str(row.get('Yabancı Dili', 'İngilizce')).strip()
        lang_code = LANG_MAP.get(lang_raw, 'tr')

        empty_quota = 0
        try:
            if pd.notna(row.get('BOŞ KONTENJAN')):
                empty_quota = int(float(str(row.get('BOŞ KONTENJAN')).replace(',', '.')))
        except:
            pass

        # Taban Puanlar (İlk Yerleştirme ve 2. Nakil)
        col_nakil = [c for c in df.columns if '2. Nakil' in str(c) or 'TABAN PUAN(2' in str(c)]
        col_ilk = [c for c in df.columns if 'İlk Yerleştirme' in str(c) or 'TABAN PUAN(İ' in str(c)]

        score_nakil = clean_score(row.get(col_nakil[0])) if col_nakil else None
        score_ilk = clean_score(row.get(col_ilk[0])) if col_ilk else None

        # Asıl taban puan olarak ilk yerleştirme veya 2. nakil (mevcut olan)
        min_score = score_ilk if score_ilk is not None else score_nakil

        cat_key = categorize_school_type(school_type)

        item = {
            'code': code,
            'city': city,
            'district': district,
            'school': school_name,
            'schoolType': school_type,
            'category': cat_key,
            'field': field_name,
            'duration': duration,
            'gender': gender,
            'boarding': boarding,
            'language': lang_raw,
            'langCode': lang_code,
            'emptyQuota': empty_quota,
            'minScore': min_score,
            'scoreFirstPlacement': score_ilk,
            'scoreSecondPlacement': score_nakil,
            'year': 2026
        }

        all_schools.append(item)
        by_category[cat_key].append(item)

        if city:
            cities.add(city)
            if district:
                districts_by_city[city].add(district)

        # Alan istatistiği
        f_key = field_name or 'Genel (Alansız)'
        f_stat = fields_map[f_key]
        f_stat['count'] += 1
        f_stat['schoolTypes'].add(school_type)
        if min_score is not None:
            f_stat['minMin'] = min(f_stat['minMin'], min_score)
            f_stat['maxMax'] = max(f_stat['maxMax'], min_score)

    # 1. Ana schools.json
    all_schools.sort(key=lambda x: (x['city'] or '', x['district'] or '', x['school']))
    all_path = os.path.join(lgs_dir, 'schools.json')
    with open(all_path, 'w', encoding='utf-8') as f:
        json.dump(all_schools, f, ensure_ascii=False, separators=(',', ':'))
    print(f"  schools.json: {len(all_schools):4d} okul programı | {os.path.getsize(all_path)/1024:8.1f} KB")

    # 2. Kategori bazlı JSON dosyaları
    cat_file_map = {
        'fen': 'schools_fen.json',
        'anadolu': 'schools_anadolu.json',
        'imamhatip': 'schools_imamhatip.json',
        'meslek': 'schools_meslek.json',
        'sosyal': 'schools_sosyal.json'
    }

    counts_by_cat = {}
    for c_key, f_name in cat_file_map.items():
        c_list = by_category[c_key]
        c_path = os.path.join(lgs_dir, f_name)
        with open(c_path, 'w', encoding='utf-8') as f:
            json.dump(c_list, f, ensure_ascii=False, separators=(',', ':'))
        counts_by_cat[c_key] = len(c_list)
        print(f"  {f_name:25s}: {len(c_list):4d} okul | {os.path.getsize(c_path)/1024:8.1f} KB")

    # 3. departments.json (Alanlar)
    departments = []
    for f_name, f_data in sorted(fields_map.items()):
        departments.append({
            'name': f_name,
            'count': f_data['count'],
            'schoolTypes': sorted(list(f_data['schoolTypes'])),
            'minMin': f_data['minMin'] if f_data['minMin'] != float('inf') else None,
            'maxMax': f_data['maxMax'] if f_data['maxMax'] != float('-inf') else None
        })
    dept_path = os.path.join(lgs_dir, 'departments.json')
    with open(dept_path, 'w', encoding='utf-8') as f:
        json.dump(departments, f, ensure_ascii=False, separators=(',', ':'))
    print(f"  departments.json: {len(departments):4d} alan/program | {os.path.getsize(dept_path)/1024:8.1f} KB")

    # 4. meta.json
    city_district_dict = {c: sorted(list(districts_by_city[c])) for c in sorted(cities)}
    valid_scores = [s['minScore'] for s in all_schools if s['minScore'] is not None]
    
    meta = {
        'name': 'LGS Merkezi Sınav Liseleri Taban Puanları',
        'source': 'T.C. Millî Eğitim Bakanlığı (MEB) e-Okul Tercih Rehberi',
        'updatedAt': '2026-08-20',
        'year': 2026,
        'totalSchools': len(all_schools),
        'countsByCategory': counts_by_cat,
        'scoreRange': {
            'min': min(valid_scores) if valid_scores else None,
            'max': max(valid_scores) if valid_scores else None,
            'avg': round(sum(valid_scores)/len(valid_scores), 2) if valid_scores else None
        },
        'totalCities': len(cities),
        'cities': sorted(list(cities)),
        'districtsByCity': city_district_dict
    }

    meta_path = os.path.join(lgs_dir, 'meta.json')
    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, separators=(',', ':'))
    print(f"  meta.json: {len(cities)} il, {sum(len(v) for v in city_district_dict.values())} ilçe")

    # 5. index.json (Şema)
    index_data = {
        'name': 'LGS Merkezi Sınav Taban Puanları ve Tercih Veri Seti',
        'year': 2026,
        'schema': {
            'code': 'Tercih Kodu (MEB)',
            'city': 'İl (81 İl)',
            'district': 'İlçe',
            'school': 'Okul Adı',
            'schoolType': 'Okul Türü (Fen, Anadolu, İmam Hatip, Mesleki ve Teknik, Sosyal Bilimler)',
            'category': 'Kategori anahtarı (fen | anadolu | imamhatip | meslek | sosyal)',
            'field': 'Alan / Bölüm Adı (ör: Bilişim Teknolojileri, Fen Bilimleri vb.)',
            'duration': 'Öğretim Süresi (4 yıl / Hazırlık + 4 yıl)',
            'gender': 'Öğretim Şekli (Kız/Erkek | Kız | Erkek)',
            'boarding': 'Pansiyon Durumu (Var / Yok / Kontenjan)',
            'language': 'Yabancı Dil (İngilizce, Almanca, Fransızca vb.)',
            'emptyQuota': 'Boş Kontenjan Sayısı',
            'minScore': 'Geçerli Taban Puan',
            'scoreFirstPlacement': 'İlk Yerleştirme Taban Puanı',
            'scoreSecondPlacement': '2. Nakil Taban Puanı'
        }
    }
    with open(os.path.join(lgs_dir, 'index.json'), 'w', encoding='utf-8') as f:
        json.dump(index_data, f, ensure_ascii=False, separators=(',', ':'))

    print(f"\n[BAŞARILI] Toplam {len(all_schools)} LGS lise programı açık veriye dönüştürüldü!")

if __name__ == '__main__':
    src = r"C:\Users\HP\Downloads\2026 lgs taban.xlsx"
    out = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    convert_lgs(src, out)
