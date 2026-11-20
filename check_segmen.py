import json
with open('analisis_rfm_kmeans.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)
cells = nb['cells']

# Print content of cells that use segmen_aturan
for idx, c in enumerate(cells):
    src = ''.join(c['source'])
    if 'segmen_aturan' in src:
        print(f"\n{'='*60}")
        print(f"CELL {idx} ({c['cell_type']}):")
        print(src[:600])
        print('...' if len(src) > 600 else '')
