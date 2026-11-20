"""
Insert Minggu 3 (Sel 15-19) into the notebook after cell 35 (Sel 14 export).
This creates r_score, f_score, m_score, rfm_score_str, and segmen_aturan columns
in rfm_table, which are required by Sel 23, 24, 25, 31.
"""
import json

NOTEBOOK = 'analisis_rfm_kmeans.ipynb'

with open(NOTEBOOK, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']
print(f"Before: {len(cells)} cells")

# Safety: abort if already present
for c in cells:
    if 'def assign_segment_rule' in ''.join(c['source']):
        print("Minggu 3 already present. Aborting.")
        raise SystemExit(0)

# ── Helper functions ──────────────────────────────────────────────────
def md(lines):
    return {"cell_type": "markdown", "metadata": {}, "source": lines}

def code(lines):
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": lines}

# ── Build 11 Minggu 3 cells ──────────────────────────────────────────

new_cells_to_insert = [
    # 1. Minggu 3 Header
    md([
        "---\n",
        "## Minggu 3: Skoring RFM dan Segmentasi Berbasis Aturan\n",
        "\n",
        "**Tujuan:** Memberikan skor pada masing-masing dimensi RFM menggunakan metode *quintile* (R dan M) serta aturan manual (F), kemudian menetapkan segmen pelanggan berdasarkan kombinasi skor tersebut tanpa algoritma Machine Learning.\n"
    ]),

    # 2. Sel 15 markdown
    md([
        "### Sel 15: Skoring Recency (R) dan Monetary (M) dengan Kuantil (pd.qcut)\n",
        "**Tujuan:** Membagi nilai R dan M menjadi 5 kelompok (quintile). Recency menggunakan label terbalik (semakin kecil hari = skor lebih tinggi).\n"
    ]),

    # 3. Sel 15 code
    code([
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
    ]),

    # 4. Sel 16 markdown
    md([
        "### Sel 16: Skoring Frequency (F) Manual dan Pembuatan String Skor RFM\n",
        "**Tujuan:** Karena distribusi *Frequency* sangat miring (mayoritas F=1), skoring F menggunakan aturan manual diskret: F=1 -> skor 1, F=2 -> skor 3, F>=3 -> skor 5.\n"
    ]),

    # 5. Sel 16 code
    code([
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
    ]),

    # 6. Sel 17 markdown
    md([
        "### Sel 17: Penetapan Segmen Berbasis Aturan (`segmen_aturan`)\n",
        "**Tujuan:** Mengelompokkan pelanggan ke dalam 5 segmen berdasarkan kombinasi skor R, F, dan M tanpa Machine Learning, sebagai *baseline* untuk perbandingan dengan K-Means.\n"
    ]),

    # 7. Sel 17 code
    code([
        "def assign_segment_rule(row):\n",
        "    \"\"\"Tetapkan 5 segmen berdasarkan kombinasi skor R, F, M.\"\"\"\n",
        "    f = row['f_score']\n",
        "    r = row['r_score']\n",
        "    m = row['m_score']\n",
        "\n",
        "    if f >= 3:                            # Frekuensi tinggi (repeat buyer)\n",
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
    ]),

    # 8. Sel 18 markdown
    md([
        "### Sel 18: Profil Agregat Segmen Berbasis Aturan\n",
        "**Tujuan:** Menghitung rata-rata dan total nilai RFM pada setiap segmen untuk memvalidasi bahwa aturan segmentasi mencerminkan karakteristik yang bermakna.\n"
    ]),

    # 9. Sel 18 code
    code([
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
    ]),

    # 10. Sel 19 markdown
    md([
        "### Sel 19: Eksport Tabel RFM dengan Skor dan Segmen (`rfm_scored.csv`)\n",
        "**Tujuan:** Menyimpan hasil skoring dan segmentasi berbasis aturan ke file CSV.\n"
    ]),

    # 11. Sel 19 code
    code([
        "SCORED_FILE = 'rfm_scored.csv'\n",
        "rfm_table.to_csv(SCORED_FILE, index=False)\n",
        "print(f'Tabel RFM ber-skor berhasil diekspor ke: {SCORED_FILE}')\n",
        "print(f'Dimensi: {rfm_table.shape[0]} baris, {rfm_table.shape[1]} kolom.')\n",
        "print('Kolom tersedia:', list(rfm_table.columns))\n"
    ]),
]

# ── Insert after cell 35 (Sel 14 code), before cell 36 (Minggu 4 header) ──
INSERT_AT = 36  # Insert BEFORE this index
final_cells = cells[:INSERT_AT] + new_cells_to_insert + cells[INSERT_AT:]

nb['cells'] = final_cells
print(f"After: {len(final_cells)} cells (inserted {len(new_cells_to_insert)} cells at index {INSERT_AT})")

# ── Save ──────────────────────────────────────────────────────────────
with open(NOTEBOOK, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print("Notebook saved successfully.")

# ── Verify ────────────────────────────────────────────────────────────
print("\n=== Verification: cells 34-62 ===")
for i in range(34, min(62, len(final_cells))):
    fl = final_cells[i]['source'][0].strip()[:70] if final_cells[i]['source'] else ''
    print(f"  {i:3d} ({final_cells[i]['cell_type'][:4]}): {fl}")
