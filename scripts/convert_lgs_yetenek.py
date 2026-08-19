# -*- coding: utf-8 -*-
"""
acik-veri / scripts / convert_lgs_yetenek.py

MEB Yetenek Sınavı ile Öğrenci Alan Liseler (Güzel Sanatlar, Spor ve Özel Proje AİHL)
Excel tablosunu standart açık veri JSON formatına dönüştürür.

Çıktı Dosyaları:
  lgs/yetenek_okullari.json       (Tüm 504 okul programı)
  lgs/yetenek_spor.json           (Spor Liseleri)
  lgs/yetenek_guzelsanatlar.json  (Güzel Sanatlar Liseleri)
  lgs/yetenek_imamhatip.json      (Musiki, Hafızlık ve Geleneksel Sanat AİHL)
"""

import json
import os
import re
import pandas as pd

def parse_quota_details(quota_str):
    """'90\nErkek :50\nKız :40' -> { total: 90, male: 50, female: 40 }"""
    if pd.isna(quota_str):
        return {'total': 0, 'male': None, 'female': None}
    
    s = str(quota_str).strip()
    lines = [l.strip() for l in s.split('\n') if l.strip()]
    
    total = 0
    male = None
    female = None
    
    if lines:
        try:
            total = int(re.search(r'\d+', lines[0]).group())
        except:
            total = 0
            
    for l in lines[1:]:
        l_lower = l.lower()
        if 'erkek' in l_lower and ':' in l:
            try:
                val = l.split(':')[1].strip()
                if val not in ('-', '--', ''):
                    male = int(re.search(r'\d+', val).group())
            except:
                pass
        elif 'kız' in l_lower and ':' in l:
            try:
                val = l.split(':')[1].strip()
                if val not in ('-', '--', ''):
                    female = int(re.search(r'\d+', val).group())
            except:
                pass
                
    return {'total': total, 'male': male, 'female': female}

def clean_boarding(boarding_str):
    if pd.isna(boarding_str):
        return 'Yok'
    s = str(boarding_str).strip()
    if 'yok' in s.lower():
        return 'Yok'
    return s

def convert_yetenek(excel_path, out_base_dir):
    lgs_dir = os.path.join(out_base_dir, 'lgs')
    os.makedirs(lgs_dir, exist_ok=True)
    
    excel = pd.ExcelFile(excel_path)
    print(f"Yetenek Sınavı Excel dosyası okunuyor: {excel_path}")
    
    all_records = []
    by_type = {
        'spor': [],
        'guzelsanat': [],
        'imamhatip': []
    }
    
    sheet_map = {
        'spor': ('spor', 'Spor Lisesi'),
        'güzel sanat': ('guzelsanat', 'Güzel Sanatlar Lisesi'),
        'aihl': ('imamhatip', 'Anadolu İmam Hatip Lisesi')
    }
    
    for s_name in excel.sheet_names:
        key_tuple = sheet_map.get(s_name.lower().strip())
        if not key_tuple:
            for k in sheet_map:
                if k in s_name.lower():
                    key_tuple = sheet_map[k]
                    break
        if not key_tuple:
            continue
            
        type_key, standard_type_name = key_tuple
        df = pd.read_excel(excel_path, sheet_name=s_name, header=4)
        
        print(f"Sheet [{s_name}] işleniyor ({len(df)} satır)...")
        
        for _, row in df.iterrows():
            city = str(row.get('İl', '')).strip()
            district = str(row.get('İlçe', '')).strip()
            school = str(row.get('Kurum Adı', '')).strip()
            field = str(row.get('Alanı', '')).strip()
            
            if not school or school == 'nan':
                continue
                
            genel_kont = parse_quota_details(row.get('Genel Kontenjan'))
            bos_kont = parse_quota_details(row.get('Boş Kontenjan'))
            boarding = clean_boarding(row.get('Pansiyon Durumu'))
            
            item = {
                'city': city,
                'district': district,
                'school': school,
                'schoolType': standard_type_name,
                'typeKey': type_key,
                'field': field,
                'quota': genel_kont['total'],
                'quotaMale': genel_kont['male'],
                'quotaFemale': genel_kont['female'],
                'emptyQuota': bos_kont['total'],
                'emptyQuotaMale': bos_kont['male'],
                'emptyQuotaFemale': bos_kont['female'],
                'boarding': boarding,
                'admissionType': 'Yetenek Sınavı (%70 Yetenek + %30 OBP)',
                'year': 2026
            }
            
            all_records.append(item)
            by_type[type_key].append(item)

    # 1. Ana dosya: yetenek_okullari.json
    all_records.sort(key=lambda x: (x['city'], x['district'], x['school']))
    all_path = os.path.join(lgs_dir, 'yetenek_okullari.json')
    with open(all_path, 'w', encoding='utf-8') as f:
        json.dump(all_records, f, ensure_ascii=False, separators=(',', ':'))
    print(f"  yetenek_okullari.json: {len(all_records):4d} okul programı | {os.path.getsize(all_path)/1024:8.1f} KB")

    # 2. Tür bazlı dosyalar
    file_target_map = {
        'spor': 'yetenek_spor.json',
        'guzelsanat': 'yetenek_guzelsanatlar.json',
        'imamhatip': 'yetenek_imamhatip.json'
    }
    
    for t_key, fname in file_target_map.items():
        data_list = by_type[t_key]
        data_list.sort(key=lambda x: (x['city'], x['district'], x['school']))
        fpath = os.path.join(lgs_dir, fname)
        with open(fpath, 'w', encoding='utf-8') as f:
            json.dump(data_list, f, ensure_ascii=False, separators=(',', ':'))
        print(f"  {fname:25s}: {len(data_list):4d} okul programı | {os.path.getsize(fpath)/1024:8.1f} KB")

    print(f"\n[BAŞARILI] Toplam {len(all_records)} Yetenek Sınavı okulu açık veri havuzuna eklendi!")

if __name__ == '__main__':
    src = r"C:\Users\HP\Downloads\özel alımlar lgs.xlsx"
    out = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    convert_yetenek(src, out)
