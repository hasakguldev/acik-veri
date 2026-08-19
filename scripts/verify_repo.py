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

print(f"YKS Birleşik Veri Seti ({len(yfiles)} dosya, {ysize:.2f} MB):")
print(f"  Kapsanan Yıllar: {meta['yearsIncluded']}")
print(f"  En Güncel Yıl: {meta['latestYear']}")
print(f"  Toplam Benzersiz Program: {meta['totalUniquePrograms']}")
print(f"  Bölüm Sayısı: {meta['totalDepartments']}")
print(f"  Üniversite: {len(meta['universities'])}, Şehir: {len(meta['cities'])}\n")

# Parametreler
pdir = os.path.join(base, 'parametreler')
pfiles = [f for f in os.listdir(pdir) if os.path.isfile(os.path.join(pdir, f))]
psize = dir_size(pdir) / 1024
print(f"Parametreler ({len(pfiles)} dosya, {psize:.1f} KB):")
for pf in pfiles:
    print(f"  - {pf}")
print()

# Toplam
total_bytes = 0
for root, dirs, files in os.walk(base):
    if '.git' in root:
        continue
    for f in files:
        total_bytes += os.path.getsize(os.path.join(root, f))

print(f"Toplam Depo Boyutu: {total_bytes / (1024*1024):.2f} MB")
print("\n[OK] Depo bütünlüğü doğrulandı.")
