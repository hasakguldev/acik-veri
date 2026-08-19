# -*- coding: utf-8 -*-
"""
acik-veri / scripts / convert_yks.py

ÖSYM YKS yerleştirme Excel tablolarını (Tablo-3 ve Tablo-4)
standart JSON formatına dönüştürür.

Kullanım:
  python scripts/convert_yks.py --t3 <tablo3.xls(x)> --t4 <tablo4.xls(x)> --year 2024

Çıktı:
  yks/<year>/meta.json
  yks/<year>/programs_tyt.json
  yks/<year>/programs_say.json
  yks/<year>/programs_ea.json
  yks/<year>/programs_soz.json
  yks/<year>/programs_dil.json
  yks/<year>/departments.json
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict

import pandas as pd

# ───────────────────────────── Sabitler ─────────────────────────────

LANG_MAP = {
    'İngilizce': 'en', 'Almanca': 'de', 'Fransızca': 'fr',
    'Arapça': 'ar', 'Rusça': 'ru', 'Çince': 'zh',
    'İtalyanca': 'it', 'İspanyolca': 'es', 'Korece': 'ko',
    'Ermenice': 'hy', 'Bulgarca': 'bg', 'Boşnakça': 'bs', 'Lehçe': 'pl',
}

SCORE_TYPE_MAP = {
    'TYT': 'TYT', 'SAY': 'SAY', 'EA': 'EA', 'SÖZ': 'SOZ', 'DİL': 'DIL',
}

SCORE_FILE = {
    'TYT': 'programs_tyt.json',
    'SAY': 'programs_say.json',
    'EA':  'programs_ea.json',
    'SOZ': 'programs_soz.json',
    'DIL': 'programs_dil.json',
}

COLS = [
    'Program Kodu', 'Üniversite Türü', 'Üniversite Adı',
    'Fakülte/Yüksekokul Adı', 'Program Adı', 'Puan Türü',
    'Kontenjan', 'Yerleşen', 'En Küçük Puan', 'En Büyük Puan',
]

# ───────────────────────── Yardımcı Fonksiyonlar ─────────────────────────

def parse_program_details(prog_str: str):
    """Program adından burs, dil ve öğretim türünü ayıklar."""
    prog_str = str(prog_str).strip()
    scholarship = 'none'
    language = 'tr'
    edu_type = 'formal'

    matches = re.findall(r'\((.*?)\)', prog_str)
    clean_prog = prog_str

    for m in matches:
        m_strip = m.strip()
        matched = False

        # Burs kontrolü
        if m_strip == 'Burslu':
            scholarship = 'full'; matched = True
        elif '%50' in m_strip:
            scholarship = '50'; matched = True
        elif '%25' in m_strip:
            scholarship = '25'; matched = True
        elif '%75' in m_strip:
            scholarship = '75'; matched = True
        elif m_strip == 'Ücretli':
            scholarship = 'none'; matched = True

        # Dil kontrolü
        if m_strip in LANG_MAP:
            language = LANG_MAP[m_strip]; matched = True

        # Öğretim türü kontrolü
        if m_strip in ('Açıköğretim', 'Uzaktan Öğretim'):
            edu_type = 'distance'; matched = True
        elif m_strip == 'İkinci Öğretim' or m_strip == 'İÖ':
            edu_type = 'evening'; matched = True

        if matched:
            clean_prog = clean_prog.replace(f'({m})', '').strip()

    clean_prog = re.sub(r'\s+', ' ', clean_prog).strip()
    return clean_prog, scholarship, language, edu_type


def parse_university_city(univ_str: str):
    """'HACETTEPE ÜNİVERSİTESİ (ANKARA)' → ('HACETTEPE ÜNİVERSİTESİ', 'ANKARA')"""
    univ_raw = str(univ_str).strip()
    m = re.search(r'^(.*?)\s*\((.*?)\)$', univ_raw)
    if m:
        return m.group(1).strip(), m.group(2).strip()
    return univ_raw, None


def is_valid_score(val) -> bool:
    if pd.isna(val):
        return False
    sval = str(val).strip()
    if sval in ('--', '---', ''):
        return False
    try:
        float(sval.replace(',', '.'))
        return True
    except ValueError:
        return False


# ───────────────────────── Ana İşlem ─────────────────────────

def convert(t3_path: str, t4_path: str, year: str, output_base: str):
    out_dir = os.path.join(output_base, 'yks', year)
    os.makedirs(out_dir, exist_ok=True)

    # 1. Excel dosyalarını oku (ilk 10 sütun: genel kontenjan bloğu)
    print(f'[{year}] Tablo-3 okunuyor: {t3_path}')
    df3 = pd.read_excel(t3_path, header=2).iloc[:, :10]
    df3.columns = COLS
    df3['Puan Türü'] = 'TYT'  # Tablo 3 = ön lisans = TYT

    print(f'[{year}] Tablo-4 okunuyor: {t4_path}')
    df4 = pd.read_excel(t4_path, header=2).iloc[:, :10]
    df4.columns = COLS

    # 2. Geçersiz puan satırlarını süz
    df3 = df3[df3['En Küçük Puan'].apply(is_valid_score) & df3['En Büyük Puan'].apply(is_valid_score)].copy()
    df4 = df4[df4['En Küçük Puan'].apply(is_valid_score) & df4['En Büyük Puan'].apply(is_valid_score)].copy()

    df_all = pd.concat([df3, df4], ignore_index=True)

    # 3. Dönüştür
    programs_by_type = {k: [] for k in SCORE_FILE}
    all_universities = set()
    all_cities = set()
    dept_data = defaultdict(lambda: {
        'count': 0,
        'scoreTypes': set(),
        'faculties': set(),
        'minMin': float('inf'),
        'maxMax': float('-inf'),
    })

    for _, row in df_all.iterrows():
        code = str(row['Program Kodu']).strip()
        univ_type = str(row['Üniversite Türü']).strip()
        university, city = parse_university_city(str(row['Üniversite Adı']))
        faculty = str(row['Fakülte/Yüksekokul Adı']).strip()
        prog_raw = str(row['Program Adı']).strip()
        score_type_raw = str(row['Puan Türü']).strip()
        score_type = SCORE_TYPE_MAP.get(score_type_raw, score_type_raw)

        try:
            quota = int(round(float(str(row['Kontenjan']).replace(',', '.'))))
            placed = int(round(float(str(row['Yerleşen']).replace(',', '.'))))
            min_score = round(float(str(row['En Küçük Puan']).replace(',', '.')), 2)
            max_score = round(float(str(row['En Büyük Puan']).replace(',', '.')), 2)
        except (ValueError, TypeError):
            continue

        clean_prog, scholarship, language, edu_type = parse_program_details(prog_raw)

        item = {
            'code': code,
            'univType': univ_type,
            'university': university,
            'city': city,
            'faculty': faculty,
            'program': clean_prog,
            'scoreType': score_type,
            'quota': quota,
            'placed': placed,
            'minScore': min_score,
            'maxScore': max_score,
            'scholarship': scholarship,
            'language': language,
            'eduType': edu_type,
        }

        if score_type in programs_by_type:
            programs_by_type[score_type].append(item)

        all_universities.add(university)
        if city:
            all_cities.add(city)

        # Bölüm istatistikleri
        dept = dept_data[clean_prog]
        dept['count'] += 1
        dept['scoreTypes'].add(score_type)
        dept['faculties'].add(faculty)
        dept['minMin'] = min(dept['minMin'], min_score)
        dept['maxMax'] = max(dept['maxMax'], max_score)

    # 4. JSON dosyalarını yaz
    counts = {}
    print(f'\n--- [{year}] JSON DOSYA RAPORU ---')

    for stype, filename in SCORE_FILE.items():
        data = programs_by_type[stype]
        path = os.path.join(out_dir, filename)
        counts[stype.lower()] = len(data)

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, separators=(',', ':'))

        size_kb = os.path.getsize(path) / 1024
        print(f'  {filename:25s}: {len(data):6d} kayıt | {size_kb:8.1f} KB')

    # 5. departments.json
    departments = []
    for name, d in sorted(dept_data.items()):
        departments.append({
            'name': name,
            'count': d['count'],
            'scoreTypes': sorted(d['scoreTypes']),
            'faculty': sorted(d['faculties'])[0] if d['faculties'] else '',
            'minMin': round(d['minMin'], 2),
            'maxMax': round(d['maxMax'], 2),
        })

    dept_path = os.path.join(out_dir, 'departments.json')
    with open(dept_path, 'w', encoding='utf-8') as f:
        json.dump(departments, f, ensure_ascii=False, separators=(',', ':'))
    print(f'  {"departments.json":25s}: {len(departments):6d} bölüm | {os.path.getsize(dept_path)/1024:8.1f} KB')

    # 6. meta.json
    meta = {
        'source': f'ÖSYM {year} YKS Yerleştirme Sonuçları (Tablo-3, Tablo-4)',
        'year': int(year),
        'generatedAt': pd.Timestamp.now().strftime('%Y-%m-%d'),
        'counts': counts,
        'totalPrograms': sum(counts.values()),
        'universities': sorted(all_universities),
        'cities': sorted(all_cities),
    }

    meta_path = os.path.join(out_dir, 'meta.json')
    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, separators=(',', ':'))
    print(f'  {"meta.json":25s}: {len(meta["universities"]):4d} üniv, {len(meta["cities"]):2d} şehir')

    total_programs = sum(counts.values())
    print(f'\n  [OK] [{year}] Toplam {total_programs} program basariyla donusturuldu.')
    return total_programs


# ───────────────────────── CLI ─────────────────────────

def main():
    parser = argparse.ArgumentParser(description='ÖSYM YKS Excel → JSON dönüştürücü')
    parser.add_argument('--t3', required=True, help='Tablo-3 (ön lisans) Excel dosyası yolu')
    parser.add_argument('--t4', required=True, help='Tablo-4 (lisans) Excel dosyası yolu')
    parser.add_argument('--year', required=True, help='Yerleştirme yılı (ör: 2025)')
    parser.add_argument('--out', default='.', help='Çıktı kök dizini (varsayılan: mevcut dizin)')
    args = parser.parse_args()

    if not os.path.exists(args.t3):
        print(f'HATA: Tablo-3 dosyası bulunamadı: {args.t3}', file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(args.t4):
        print(f'HATA: Tablo-4 dosyası bulunamadı: {args.t4}', file=sys.stderr)
        sys.exit(1)

    convert(args.t3, args.t4, args.year, args.out)


if __name__ == '__main__':
    main()
