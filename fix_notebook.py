"""
Fix: Insert Minggu 3 (Sel 15-19) after cell index 35 (Sel 14 export).
This creates segmen_aturan column needed by Sel 23, 24, 25, 31.
"""
import json

NOTEBOOK = 'analisis_rfm_kmeans.ipynb'

with open(NOTEBOOK, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']

def mk_md(src_lines):
    return {"cell_type": "markdown", "metadata": {}, "source": src_lines}

def mk_code(src_lines):
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": src_lines}

# Safety check: is segmen_aturan already defined somewhere?
for idx, c in enumerate(cells):
    src = ''.join(c['source'])
    if "assign_segment_rule" in src and "def " in src:
        print(f"WARNING: Minggu 3 already exists at cell {idx}. Aborting.")
        raise SystemExit(0)

# ── Build Minggu 3 cells ─────────────────────────────────────────────

minggu3_header = mk_md([
    "---\n",
    "## Minggu 3: Skoring RFM dan Segmentasi Berbasis Aturan\n",
    "\n",
    "**Tujuan:** Memberikan skor pada masing-masing dimensi RFM menggunakan metode *quintile* (R dan M) serta aturan manual (F), kemudian menetapkan segmen pelanggan berdasarkan kombinasi skor tersebut tanpa algoritma Machine Learning.\n",
    "\n",
    "**Tahapan Kerja:**\n",
    "1. **Skoring R:** Pemberian skor 1\u20135 pada `recency_hari` menggunakan `pd.qcut` dengan label terbalik (5 = paling baru).\n",
    "2. **Skoring M:** Pemberian skor 1\u20135 pada `monetary_rp` menggunakan `pd.qcut` (5 = nilai tertinggi).\n",
    "3. **Skoring F:** Pemberian skor manual berdasarkan frekuensi transaksi (F=1\u21921, F=2\u21923, F\u22653\u21925).\n",
    "4. **Segmentasi Aturan:** Menetapkan 5 segmen berdasarkan kombinasi skor R, F, dan M.\n",
    "5. **Ekspor:** Menyimpan tabel RFM beserta skor dan label segmen ke `rfm_scored.csv`.\n"
])

md_sel15 = mk_md([
    "### Sel 15: Skoring Recency (R) dan Monetary (M) dengan Kuantil (pd.qcut)\n",
    "**Tujuan:** Membagi nilai R dan M menjadi 5 kelompok (quintile) yang setara populasinya. ",
    "Recency menggunakan label terbalik (semakin kecil hari \u2192 skor lebih tinggi).\n"
])

code_sel15 = mk_code([
    "# --- Skoring R: semakin kecil recency_hari, semakin tinggi skor (terbalik) ---\n",
    "rfm_table['r_score'] = pd.qcut(\n",
    "    rfm_table['recency_hari'],\n",
    "    q=5,\n",
    "    labels=[5, 4, 3, 2, 1],   # label terbalik: hari kecil = skor besar\n",
    "    duplicates='drop'\n",
    ").astype(int)\n",
    "\n",
    "# --- Skoring M: semakin besar monetary, semakin tinggi skor ---\n",
    "rfm_table['m_score'] = pd.qcut(\n",
    "    rfm_table['monetary_rp'],\n",
    "    q=5,\n",
    "    labels=[1, 2, 3, 4, 5],\n",
    "    duplicates='drop'\n",
    ").astype(int)\n",
    "\n",
    "print('Distribusi R-Score:')\n",
    "print(rfm_table['r_score'].value_counts().sort_index())\n",
    "print('\\nDistribusi M-Score:')\n",
    "print(rfm_table['m_score'].value_counts().sort_index())\n"
])

md_sel16 = mk_md([
    "### Sel 16: Skoring Frequency (F) Manual dan Pembuatan String Skor RFM\n",
    "**Tujuan:** Karena distribusi *Frequency* sangat miring (mayoritas F=1), skoring F ",
    "menggunakan aturan manual diskret: F=1\u21921, F=2\u21923, F\u22653\u21925.\n"
])

code_sel16 = mk_code([
    "# --- Skoring F: manual berdasarkan jumlah transaksi ---\n",
    "def score_frequency(f):\n",
    "    if f == 1:\n",
    "        return 1\n",
    "    elif f == 2:\n",
    "        return 3\n",
    "    else:          # f >= 3\n",
    "        return 5\n",
    "\n",
    "rfm_table['f_score'] = rfm_table['frequency'].apply(score_frequency)\n",
    "\n",
    "# --- Gabungkan menjadi string skor RFM (mis. '5-1-3') ---\n",
    "rfm_table['rfm_score_str'] = (\n",
    "    rfm_table['r_score'].astype(str) + '-' +\n",
    "    rfm_table['f_score'].astype(str) + '-' +\n",
    "    rfm_table['m_score'].astype(str)\n",
    ")\n",
    "\n",
    "print('Distribusi F-Score:')\n",
    "print(rfm_table['f_score'].value_counts().sort_index())\n",
    "print('\\nSampel 5 baris dengan kolom skor RFM:')\n",
    "print(rfm_table[['id_pembeli', 'recency_hari', 'frequency', 'monetary_rp',\n",
    "                   'r_score', 'f_score', 'm_score', 'rfm_score_str']].head())\n"
])

md_sel17 = mk_md([
    "### Sel 17: Penetapan Segmen Berbasis Aturan (`segmen_aturan`)\n",
    "**Tujuan:** Mengelompokkan pelanggan ke dalam 5 segmen berdasarkan kombinasi skor R, F, dan M ",
    "tanpa Machine Learning \u2014 sebagai *baseline* untuk perbandingan dengan K-Means.\n"
])

code_sel17 = mk_code([
    "def assign_segment_rule(row):\n",
    "    \"\"\"Tetapkan 5 segmen berdasarkan kombinasi skor R, F, M.\"\"\"\n",
    "    f = row['f_score']\n",
    "    r = row['r_score']\n",
    "    m = row['m_score']\n",
    "\n",
    "    if f >= 3:                            # Frekuensi tinggi\n",
    "        return 'Pelanggan Loyal'\n",
    "    elif f == 1 and r >= 4 and m >= 3:   # Baru, belanja besar\n",
    "        return 'Pembeli Potensial'\n",
    "    elif f == 1 and r >= 4 and m <= 2:   # Baru, belanja kecil\n",
    "        return 'Pembeli Baru'\n",
    "    elif f == 1 and r in [2, 3]:          # Mulai jarang kembali\n",
    "        return 'Berisiko (At Risk)'\n",
    "    else:                                 # f == 1 and r == 1\n",
    "        return 'Tidak Aktif (Lost)'\n",
    "\n",
    "rfm_table['segmen_aturan'] = rfm_table.apply(assign_segment_rule, axis=1)\n",
    "\n",
    "print('Distribusi Segmen Berbasis Aturan:')\n",
    "print(rfm_table['segmen_aturan'].value_counts())\n",
    "print('\\nProporsi Tiap Segmen (%):')\n",
    "print((rfm_table['segmen_aturan'].value_counts() / len(rfm_table) * 100).round(2))\n"
])

md_sel18 = mk_md([
    "### Sel 18: Profil Agregat Segmen Berbasis Aturan\n",
    "**Tujuan:** Menghitung rata-rata dan total nilai RFM pada setiap segmen untuk memvalidasi ",
    "bahwa aturan segmentasi mencerminkan karakteristik yang bermakna.\n"
])

code_sel18 = mk_code([
    "profil_aturan = rfm_table.groupby('segmen_aturan').agg(\n",
    "    jumlah_pembeli=('id_pembeli', 'count'),\n",
    "    rata_recency_hari=('recency_hari', 'mean'),\n",
    "    rata_frequency=('frequency', 'mean'),\n",
    "    rata_monetary_rp=('monetary_rp', 'mean'),\n",
    "    total_monetary_rp=('monetary_rp', 'sum')\n",
    ").reset_index()\n",
    "\n",
    "profil_aturan['persen_pembeli'] = (\n",
    "    (profil_aturan['jumlah_pembeli'] / len(rfm_table)) * 100\n",
    ").apply(lambda x: f'{x:.1f}%')\n",
    "profil_aturan['persen_omzet'] = (\n",
    "    (profil_aturan['total_monetary_rp'] / rfm_table['monetary_rp'].sum()) * 100\n",
    ").apply(lambda x: f'{x:.1f}%')\n",
    "\n",
    "print('Profil Rata-rata RFM per Segmen Aturan:')\n",
    "print(profil_aturan[['segmen_aturan', 'jumlah_pembeli', 'persen_pembeli',\n",
    "                       'rata_recency_hari', 'rata_frequency', 'rata_monetary_rp',\n",
    "                       'persen_omzet']].to_string(index=False))\n"
])

md_sel19 = mk_md([
    "### Sel 19: Eksport Tabel RFM dengan Skor dan Segmen (`rfm_scored.csv`)\n",
    "**Tujuan:** Menyimpan hasil skoring dan segmentasi berbasis aturan ke file CSV untuk ",
    "keperluan pelaporan dan perbandingan dengan hasil K-Means.\n"
])

code_sel19 = mk_code([
    "SCORED_FILE = 'rfm_scored.csv'\n",
    "rfm_table.to_csv(SCORED_FILE, index=False)\n",
    "print(f'Tabel RFM ber-skor berhasil diekspor ke: {SCORED_FILE}')\n",
    "print(f'Dimensi: {rfm_table.shape[0]} baris, {rfm_table.shape[1]} kolom.')\n",
    "print('Kolom tersedia:', list(rfm_table.columns))\n"
])

# ── Assemble 11 new cells ────────────────────────────────────────────
minggu3_cells = [
    minggu3_header,
    md_sel15, code_sel15,
    md_sel16, code_sel16,
    md_sel17, code_sel17,
    md_sel18, code_sel18,
    md_sel19, code_sel19,
]

# Insert AFTER cell 35 (Sel 14 export code), BEFORE cell 36 (Minggu 4 header)
INSERT_AFTER = 35
new_cells = cells[:INSERT_AFTER + 1] + minggu3_cells + cells[INSERT_AFTER + 1:]

print(f"Before: {len(cells)} cells")
print(f"Inserting {len(minggu3_cells)} cells after index {INSERT_AFTER}")
print(f"After:  {len(new_cells)} cells")

# ── Also fix val_z bug if present in cluster vis cell ─────────────────
fixed_vz = 0
for i, c in enumerate(new_cells):
    if c['cell_type'] == 'code':
        src_joined = ''.join(c['source'])
        if 'val_z:+.2f' in src_joined:
            fixed_src = src_joined.replace('val_z:+.2f', 'z_val:+.2f')
            new_cells[i]['source'] = fixed_src.split('\n')
            new_cells[i]['source'] = [line + '\n' for line in fixed_src.split('\n')]
            # Remove trailing \n from last line
            if new_cells[i]['source'][-1] == '\n':
                new_cells[i]['source'] = new_cells[i]['source'][:-1]
            fixed_vz += 1
            print(f"Fixed val_z -> z_val bug in cell {i}")

if fixed_vz == 0:
    print("Note: val_z bug not found (already fixed or pattern differs)")

# ── Save ──────────────────────────────────────────────────────────────
nb['cells'] = new_cells
with open(NOTEBOOK, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print(f"\nNotebook saved: {len(new_cells)} total cells.")

# ── Verify new structure ──────────────────────────────────────────────
print("\n=== NEW STRUCTURE (cells 33-62) ===")
for i in range(33, min(62, len(new_cells))):
    fl = new_cells[i]['source'][0].strip()[:70] if new_cells[i]['source'] else ''
    print(f"  {i:3d} ({new_cells[i]['cell_type'][:4]}): {fl}")
