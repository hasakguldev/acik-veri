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

print('=== ACIK-VERI DEPO YAPISI ===')
print()

with open(os.path.join(base, 'manifest.json'), 'r', encoding='utf-8') as f:
    m = json.load(f)
ver = m['version']
ds = list(m['datasets'].keys())
print('manifest.json v' + ver)
print('  Veri setleri: ' + str(ds))
print()

for year in ['2025', '2026']:
    ydir = os.path.join(base, 'yks', year)
    if os.path.exists(ydir):
        files = os.listdir(ydir)
        size_mb = dir_size(ydir) / (1024 * 1024)
        meta_path = os.path.join(ydir, 'meta.json')
        if os.path.exists(meta_path):
            with open(meta_path, 'r', encoding='utf-8') as f:
                meta = json.load(f)
            total = meta.get('totalPrograms', sum(meta.get('counts', {}).values()))
            univs = len(meta.get('universities', []))
            cities = len(meta.get('cities', []))
            print('yks/' + year + '/  (' + str(len(files)) + ' dosya, ' + '{:.2f}'.format(size_mb) + ' MB)')
            print('  Toplam: ' + str(total) + ' program, ' + str(univs) + ' universite, ' + str(cities) + ' sehir')

print()

pdir = os.path.join(base, 'parametreler')
pfiles = os.listdir(pdir)
psize = dir_size(pdir) / 1024
print('parametreler/  (' + str(len(pfiles)) + ' dosya, ' + '{:.1f}'.format(psize) + ' KB)')
print()

sdir = os.path.join(base, 'scripts')
sfiles = os.listdir(sdir)
print('scripts/  (' + str(len(sfiles)) + ' dosya)')
for sf in sfiles:
    print('  - ' + sf)
print()

total_bytes = 0
for root, dirs, files in os.walk(base):
    if '.git' in root:
        continue
    for f in files:
        total_bytes += os.path.getsize(os.path.join(root, f))
print('Toplam depo boyutu (git haric): ' + '{:.2f}'.format(total_bytes / (1024*1024)) + ' MB')
