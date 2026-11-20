import json
with open('analisis_rfm_kmeans.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)
cells = nb['cells']
print(f'Total cells: {len(cells)}')
print()
for idx, c in enumerate(cells):
    src = c['source']
    fl = src[0].strip()[:70] if src else ''
    ctype = c['cell_type'][:4]
    print(f'{idx:3d} ({ctype}): {fl}')
