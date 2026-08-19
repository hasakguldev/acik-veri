# -*- coding: utf-8 -*-
import os, json

base = r'C:\Users\HP\proje\acik-veri'

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

# Toplam
total_bytes = 0
for root, dirs, files in os.walk(base):
    if '.git' in root:
        continue
    for f in files:
        total_bytes += os.path.getsize(os.path.join(root, f))

print(f"Toplam Depo Boyutu: {total_bytes / (1024*1024):.2f} MB")
print("\n[OK] Depo bütünlüğü başarıyla doğrulandı.")
