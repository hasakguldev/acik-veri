# -*- coding: utf-8 -*-
import os, json

_yerel = r'C:\Users\HP\proje\acik-veri'
base = _yerel if os.path.isdir(_yerel) else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def dir_size(path):
    total = 0
    for f in os.listdir(path):
        fp = os.path.join(path, f)
        if os.path.isfile(fp):
            total += os.path.getsize(fp)
    return total

print('=== ACIK-VERI MERKEZI DEPO RAPORU ===\n')

with open(os.path.join(base, 'manifest.json'), 'r', encoding='utf-8') as f:
    m = json.load(f)

print(f"Manifest Sürümü: v{m['version']}")
print(f"CDN Adresi: {m['cdn']}")
print(f"Katalog Veri Setleri: {list(m['datasets'].keys())}\n")

# YKS
ydir = os.path.join(base, 'yks')
yfiles = [f for f in os.listdir(ydir) if os.path.isfile(os.path.join(ydir, f))]
ysize = dir_size(ydir) / (1024 * 1024)

meta_path = os.path.join(ydir, 'meta.json')
with open(meta_path, 'r', encoding='utf-8') as f:
    meta = json.load(f)

print(f"1. YKS Birleşik Veri Seti ({len(yfiles)} dosya, {ysize:.2f} MB):")
print(f"   Kapsanan Yıllar: {meta['yearsIncluded']}")
print(f"   Toplam Benzersiz Program: {meta['totalUniquePrograms']}")
print(f"   Bölüm Sayısı: {meta['totalDepartments']}")
print(f"   Üniversite: {len(meta['universities'])}, Şehir: {len(meta['cities'])}\n")

# LGS
ldir = os.path.join(base, 'lgs')
lfiles = [f for f in os.listdir(ldir) if os.path.isfile(os.path.join(ldir, f))]
lsize = dir_size(ldir) / (1024 * 1024)

lgs_meta_path = os.path.join(ldir, 'meta.json')
with open(lgs_meta_path, 'r', encoding='utf-8') as f:
    lgs_meta = json.load(f)

print(f"2. LGS Lise Taban Puanları Veri Seti ({len(lfiles)} dosya, {lsize:.2f} MB):")
print(f"   Toplam Okul/Program: {lgs_meta['totalSchools']}")
print(f"   Kategori Dağılımı: {lgs_meta['countsByCategory']}")
print(f"   Kapsam: {lgs_meta['totalCities']} İl, {sum(len(v) for v in lgs_meta['districtsByCity'].values())} İlçe\n")

# Parametreler
pdir = os.path.join(base, 'parametreler')
pfiles = [f for f in os.listdir(pdir) if os.path.isfile(os.path.join(pdir, f))]
psize = dir_size(pdir) / 1024
print(f"3. Parametreler ({len(pfiles)} dosya, {psize:.1f} KB):")
for pf in pfiles:
    print(f"   - {pf}")
print()

# Adres (il / ilçe / mahalle)
adir = os.path.join(base, 'adres')
with open(os.path.join(adir, 'meta.json'), 'r', encoding='utf-8') as f:
    ameta = json.load(f)
with open(os.path.join(adir, 'iller.json'), 'r', encoding='utf-8') as f:
    aller = json.load(f)
kimlikler = set()
toplam = 0
for il in aller:
    with open(os.path.join(adir, 'mahalleler', f"{il['kod']}.json"), 'r', encoding='utf-8') as f:
        ilv = json.load(f)
    assert len(ilv['ilceler']) == il['ilceSayisi'], f"{il['kod']}: ilçe sayısı tutmuyor"
    for ilce in ilv['ilceler']:
        assert ilce['id'] not in kimlikler, f"Yinelenen kimlik: {ilce['id']}"
        kimlikler.add(ilce['id'])
        for m in ilce['mahalleler']:
            assert m[0] not in kimlikler, f"Yinelenen kimlik: {m[0]}"
            kimlikler.add(m[0])
            toplam += 1
assert len(aller) == 81, 'Adres: 81 il beklenir'
assert toplam == ameta['counts']['toplam'], 'Adres: meta sayısı tutmuyor'
print(f"4. Adres (il/ilçe/mahalle) — kaynak {ameta['source']} ({ameta['sourceDate']}):")
print(f"   {ameta['counts']['il']} il, {ameta['counts']['ilce']} ilçe, {toplam} mahalle/köy; kimlikler eşsiz\n")

# Toplam
total_bytes = 0
for root, dirs, files in os.walk(base):
    if '.git' in root:
        continue
    for f in files:
        total_bytes += os.path.getsize(os.path.join(root, f))

print(f"Toplam Depo Boyutu: {total_bytes / (1024*1024):.2f} MB")
print("\n[OK] Depo bütünlüğü başarıyla doğrulandı.")
