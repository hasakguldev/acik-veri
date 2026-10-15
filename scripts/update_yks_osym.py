# -*- coding: utf-8 -*-
"""
acik-veri / scripts / update_yks_osym.py

Birleşik YKS dosyalarını (yks/programs_*.json) ÖSYM'nin yayımladığı
"En Küçük ve En Büyük Puanlar" tablolarıyla günceller.

Ne yapar:
  1. Merkezi yerleştirme Tablo-3/4: yılın geçmiş satırını yazar. Puan
     oluşmayan (hiç yerleşen olmayan) programlar da kontenjanıyla girer;
     minScore/maxScore null kalır. Böylece "bu yıl açıldı ama dolmadı"
     bilgisi kaybolmaz ve önceki yılın puanı bu yılınmış gibi görünmez.
  2. Ek yerleştirme Tablo-3/4 (isteğe bağlı): aynı yıl satırına
     `ek: {quota, placed, minScore, maxScore}` ekler (genel ek kontenjan).
  3. Başarı sırası ölçülmemiş yıllara kopyalanmış minRank değerlerini
     temizler (ÖSYM bu tablolarda sıra yayımlamaz).
  4. departments.json ve meta.json dosyalarını yeniden üretir.

Ardından hafif indeks yeniden üretilmelidir:
  python scripts/build_light_index.py

Kullanım:
  python scripts/update_yks_osym.py --year 2026 \
      --t3 <tablo-3.xlsx> --t4 <tablo-4.xlsx> \
      [--ek-t3 <ek-tablo-3.xlsx> --ek-t4 <ek-tablo-4.xlsx>] \
      [--rank-max-year 2024]
"""

import argparse
import datetime
import json
import os
import sys
from collections import defaultdict

import pandas as pd

from convert_yks import parse_program_details, parse_university_city, SCORE_TYPE_MAP

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
YKS = os.path.join(KOK, 'yks')
PUAN_TURLERI = ['tyt', 'say', 'ea', 'soz', 'dil']


def sayi(v):
    """'--', boş ve metin değerleri None'a çevirir."""
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return None
    s = str(v).strip().replace(',', '.')
    if s in ('', '--', '---'):
        return None
    try:
        return float(s)
    except ValueError:
        return None


def tamsayi(v):
    x = sayi(v)
    return None if x is None else int(round(x))


def puan(v):
    x = sayi(v)
    return None if x is None else round(x, 2)


def tablo_oku(yol):
    """ÖSYM tablosunu kod → satır sözlüğüne çevirir (ilk 3 satır başlık)."""
    df = pd.read_excel(yol, header=None, skiprows=3, dtype=str)
    satirlar = {}
    for _, r in df.iterrows():
        kod = str(r[0]).strip()
        if kod.isdigit():
            satirlar[kod] = r
    return satirlar


def yeni_program(kod, r):
    university, city = parse_university_city(str(r[2]))
    program, scholarship, language, edu_type = parse_program_details(str(r[4]))
    puan_turu = str(r[5]).strip()
    return {
        'code': kod,
        'univType': str(r[1]).strip(),
        'university': university,
        'city': city,
        'faculty': str(r[3]).strip(),
        'program': program,
        'scoreType': SCORE_TYPE_MAP.get(puan_turu, puan_turu),
        'scholarship': scholarship,
        'language': language,
        'eduType': edu_type,
        'history': [],
        'rankTrend': None,
        'projectedRank': None,
        'latest': None,
    }


def puanli_son(gecmis):
    """Taban puanı olan en güncel geçmiş satırı."""
    return next((h for h in gecmis if h.get('minScore') is not None), None)


def main():
    ap = argparse.ArgumentParser(description='ÖSYM puan tablolarıyla birleşik YKS verisini günceller')
    ap.add_argument('--year', type=int, required=True)
    ap.add_argument('--t3', required=True, help='Merkezi yerleştirme Tablo-3 (ön lisans)')
    ap.add_argument('--t4', required=True, help='Merkezi yerleştirme Tablo-4 (lisans)')
    ap.add_argument('--ek-t3', help='Ek yerleştirme Tablo-3')
    ap.add_argument('--ek-t4', help='Ek yerleştirme Tablo-4')
    ap.add_argument('--rank-max-year', type=int, default=2024,
                    help='Başarı sırasının gerçekten ölçüldüğü son yıl; sonrasındaki minRank kopyaları silinir')
    args = ap.parse_args()

    yil = args.year
    ana = {}
    for yol in (args.t3, args.t4):
        print(f'Okunuyor: {os.path.basename(yol)}')
        ana.update(tablo_oku(yol))
    ek = {}
    for yol in (args.ek_t3, args.ek_t4):
        if yol:
            print(f'Okunuyor: {os.path.basename(yol)}')
            ek.update(tablo_oku(yol))

    # Mevcut birleşik veriyi yükle
    programlar = {}
    tur_of = {}
    for t in PUAN_TURLERI:
        with open(os.path.join(YKS, f'programs_{t}.json'), encoding='utf-8') as f:
            for p in json.load(f):
                programlar[p['code']] = p
                tur_of[p['code']] = t

    sayac = defaultdict(int)

    for kod, r in ana.items():
        if kod not in programlar:
            p = yeni_program(kod, r)
            t = p['scoreType'].lower()
            if t not in PUAN_TURLERI:
                sayac['bilinmeyen_tur'] += 1
                continue
            programlar[kod] = p
            tur_of[kod] = t
            sayac['yeni_program'] += 1
        p = programlar[kod]

        satir = {
            'quota': tamsayi(r[6]),
            'placed': tamsayi(r[7]),
            'minScore': puan(r[8]),
            'maxScore': puan(r[9]),
            'minRank': None,
        }
        e = ek.get(kod)
        if e is not None and tamsayi(e[6]) is not None:
            satir['ek'] = {
                'quota': tamsayi(e[6]),
                'placed': tamsayi(e[7]),
                'minScore': puan(e[8]),
                'maxScore': puan(e[9]),
            }
            sayac['ek_kontenjan'] += 1
            if satir['ek']['minScore'] is not None:
                sayac['ek_puan'] += 1

        mevcut = next((h for h in p['history'] if h.get('year') == yil), None)
        if mevcut is None:
            sayac['yil_satiri_eklendi'] += 1
            satir['year'] = yil
            p['history'].append(satir)
        else:
            if any(mevcut.get(k) != satir[k] for k in ('quota', 'placed', 'minScore', 'maxScore')):
                sayac['yil_satiri_degisti'] += 1
            for k in ('quota', 'placed', 'minScore', 'maxScore'):
                mevcut[k] = satir[k]
            if 'ek' in satir:
                mevcut['ek'] = satir['ek']
            else:
                mevcut.pop('ek', None)
        if satir['minScore'] is None:
            sayac['dolmayan'] += 1

    ek_yalniz = [k for k in ek if k not in ana]
    if ek_yalniz:
        print(f'  ! Ek tabloda olup ana tabloda olmayan {len(ek_yalniz)} program atlandı')

    # Sıra kopyalarını temizle, geçmişi sırala, latest'i kur
    for p in programlar.values():
        for h in p['history']:
            if h.get('year', 0) > args.rank_max_year and h.get('minRank') is not None:
                h['minRank'] = None
                sayac['sira_kopyasi_silindi'] += 1
            h.setdefault('minRank', None)
        p['history'].sort(key=lambda h: h['year'], reverse=True)
        # Alan sırasını sabitle (year sonda, ek en sonda)
        p['history'] = [
            {k: h[k] for k in ('quota', 'placed', 'minScore', 'maxScore', 'minRank', 'year', 'ek') if k in h}
            for h in p['history']
        ]
        p['latest'] = p['history'][0] if p['history'] else None
        # latest anahtarı her zaman en sonda dursun
        p['latest'] = p.pop('latest')

    # Yaz
    sayimlar = {}
    universiteler, sehirler = set(), set()
    bolumler = defaultdict(lambda: {'count': 0, 'scoreTypes': set(), 'faculties': set(),
                                    'minMin': None, 'maxMax': None, 'bestRank': None})
    toplam = 0
    for t in PUAN_TURLERI:
        liste = sorted((p for k, p in programlar.items() if tur_of[k] == t),
                       key=lambda x: (x.get('university') or '', x.get('program') or ''))
        yol = os.path.join(YKS, f'programs_{t}.json')
        with open(yol, 'w', encoding='utf-8') as f:
            json.dump(liste, f, ensure_ascii=False, separators=(',', ':'))
        sayimlar[t] = len(liste)
        toplam += len(liste)
        print(f'  programs_{t}.json: {len(liste):6d} program | {os.path.getsize(yol)/1024:8.1f} KB')

        for p in liste:
            if p.get('university'):
                universiteler.add(p['university'])
            if p.get('city'):
                sehirler.add(p['city'])
            son = puanli_son(p['history'])
            if son is None:
                continue  # hiç taban puanı olmayan program bölüm istatistiğine girmez
            d = bolumler[p['program']]
            d['count'] += 1
            d['scoreTypes'].add(p.get('scoreType') or t.upper())
            if p.get('faculty'):
                d['faculties'].add(p['faculty'])
            d['minMin'] = son['minScore'] if d['minMin'] is None else min(d['minMin'], son['minScore'])
            if son.get('maxScore') is not None:
                d['maxMax'] = son['maxScore'] if d['maxMax'] is None else max(d['maxMax'], son['maxScore'])
            sira = next((h['minRank'] for h in p['history'] if h.get('minRank') is not None), None)
            if sira is not None:
                d['bestRank'] = sira if d['bestRank'] is None else min(d['bestRank'], sira)

    departments = [{
        'name': ad,
        'count': d['count'],
        'scoreTypes': sorted(d['scoreTypes']),
        'faculty': sorted(d['faculties'])[0] if d['faculties'] else '',
        'minMin': round(d['minMin'], 2),
        'maxMax': round(d['maxMax'], 2) if d['maxMax'] is not None else None,
        'bestRank': d['bestRank'],
    } for ad, d in sorted(bolumler.items())]
    with open(os.path.join(YKS, 'departments.json'), 'w', encoding='utf-8') as f:
        json.dump(departments, f, ensure_ascii=False, separators=(',', ':'))
    print(f'  departments.json: {len(departments)} bölüm')

    meta_yol = os.path.join(YKS, 'meta.json')
    with open(meta_yol, encoding='utf-8') as f:
        meta = json.load(f)
    kaynaklar = [os.path.basename(x) for x in (args.t3, args.t4, args.ek_t3, args.ek_t4) if x]
    meta.update({
        'updatedAt': datetime.date.today().isoformat(),
        'counts': sayimlar,
        'totalUniquePrograms': toplam,
        'totalDepartments': len(departments),
        'universities': sorted(universiteler),
        'cities': sorted(sehirler),
        'scoreSource': f'ÖSYM {yil} YKS Merkezi Yerleştirme ve Ek Yerleştirme En Küçük ve En Büyük Puanlar (Tablo-3, Tablo-4)',
        'scoreSourceFiles': kaynaklar,
        'ekPlacementYear': yil if ek else meta.get('ekPlacementYear'),
        'rankMaxYear': args.rank_max_year,
    })
    if yil not in meta.get('yearsIncluded', []):
        meta['yearsIncluded'] = sorted(set(meta.get('yearsIncluded', [])) | {yil})
    meta['latestYear'] = max(meta['yearsIncluded'])
    with open(meta_yol, 'w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, separators=(',', ':'))

    print('\nÖzet:')
    for k, v in sorted(sayac.items()):
        print(f'  {k:22s}: {v}')
    print(f'  {"toplam_program":22s}: {toplam}')


if __name__ == '__main__':
    sys.exit(main())
