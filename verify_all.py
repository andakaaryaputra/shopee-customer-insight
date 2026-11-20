"""
Verify: run ALL code cells end-to-end, check Sel 23 passes.
"""
import json, sys, traceback
import matplotlib
matplotlib.use('Agg')

NOTEBOOK = 'analisis_rfm_kmeans.ipynb'

with open(NOTEBOOK, 'r', encoding='utf-8') as f:
    nb = json.load(f)
cells = nb['cells']
print(f"Total cells: {len(cells)}")

ns = {}
code_num = 0
errors = []

for idx, c in enumerate(cells):
    if c['cell_type'] != 'code':
        continue
    code_num += 1
    src = ''.join(c['source'])
    first_line = src.split('\n')[0][:55]
    try:
        exec(compile(src, f'<cell_{idx}>', 'exec'), ns)
    except Exception as e:
        err_msg = f"Cell {idx} (code #{code_num}): {type(e).__name__}: {e}"
        errors.append(err_msg)
        print(f"  ERROR at {err_msg}")
        if 'segmen_aturan' in str(e):
            traceback.print_exc()

if errors:
    print(f"\n=== {len(errors)} ERROR(S) FOUND ===")
    for e in errors:
        print(f"  {e}")
else:
    print(f"\n=== ALL {code_num} CODE CELLS PASSED! ===")

# Check rfm_table columns
if 'rfm_table' in ns:
    rt = ns['rfm_table']
    print(f"\nrfm_table columns: {list(rt.columns)}")
    if 'segmen_aturan' in rt.columns:
        print(f"segmen_aturan OK: {rt['segmen_aturan'].nunique()} unique segments")
