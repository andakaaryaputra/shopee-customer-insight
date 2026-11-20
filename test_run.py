"""
Verify notebook structure and test-run all code cells end-to-end to find the actual error.
"""
import json, sys, traceback

NOTEBOOK = 'analisis_rfm_kmeans.ipynb'

with open(NOTEBOOK, 'r', encoding='utf-8') as f:
    nb = json.load(f)
cells = nb['cells']

print(f"Total cells: {len(cells)}")

# 1. Check if Minggu 3 is present
has_assign = False
has_segmen_col = False
for idx, c in enumerate(cells):
    src = ''.join(c['source'])
    if 'def assign_segment_rule' in src:
        has_assign = True
        print(f"[OK] assign_segment_rule found at cell {idx}")
    if "rfm_table['segmen_aturan']" in src and '= rfm_table.apply' in src:
        has_segmen_col = True
        print(f"[OK] segmen_aturan column creation at cell {idx}")

if not has_assign:
    print("[MISSING] assign_segment_rule not found!")
if not has_segmen_col:
    print("[MISSING] segmen_aturan column creation not found!")

# 2. Find Sel 23 cell index
sel23_idx = None
for idx, c in enumerate(cells):
    src = ''.join(c['source'])
    if 'compute_ari' in src and 'def compute_ari' in src and 'stability_summary' in src:
        sel23_idx = idx
        print(f"\nSel 23 code is at cell index {idx}")
        break

# 3. Run all code cells up to and including Sel 23
print("\n=== Running all code cells up to Sel 23 ===")
import matplotlib
matplotlib.use('Agg')

ns = {}
code_cell_num = 0
for idx, c in enumerate(cells):
    if c['cell_type'] != 'code':
        continue
    code_cell_num += 1
    src = ''.join(c['source'])
    first_line = src.split('\n')[0][:60]
    try:
        exec(compile(src, f'<cell_{idx}>', 'exec'), ns)
        status = "OK"
    except Exception as e:
        status = f"ERROR: {type(e).__name__}: {e}"
        print(f"  Cell {idx:3d} (code #{code_cell_num:2d}): {first_line}")
        print(f"    -> {status}")
        if idx == sel23_idx:
            print(f"\n=== FULL TRACEBACK FOR SEL 23 ===")
            traceback.print_exc()
            break
        # Continue to see if later cells also fail
        continue
    
    if idx == sel23_idx:
        print(f"  Cell {idx:3d} (code #{code_cell_num:2d}): {first_line}")
        print(f"    -> {status}")
        print("\n=== Sel 23 PASSED! ===")
        break

# 4. Check if segmen_aturan exists in rfm_table at this point
if 'rfm_table' in ns:
    rt = ns['rfm_table']
    print(f"\nrfm_table columns: {list(rt.columns)}")
    if 'segmen_aturan' in rt.columns:
        print(f"[OK] segmen_aturan exists with {rt['segmen_aturan'].nunique()} unique values")
        print(rt['segmen_aturan'].value_counts())
    else:
        print("[MISSING] segmen_aturan NOT in rfm_table columns!")
