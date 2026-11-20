# Catatan Exploratory Data Analysis (EDA) Fitur RFM (Minggu 2)

**Tanggal Penyusunan:** 18 November 2026  
**File Sumber:** `data_bersih.csv`  
**File Hasil:** `rfm_table.csv`  
**Notebook:** `analisis_rfm_kmeans.ipynb` (Bagian Minggu 2)  

---

## 1. Definisi & Parameter Feature Engineering RFM
Sesuai metodologi yang ditetapkan pada [Readme.md](file:///c:/Users/ACER/Documents/RSI%20PROJECT/Readme.md) dan tidak diubah pasca-eksekusi:
- **Populasi Data:** Hanya pesanan unik berstatus `Selesai` (261 nomor pesanan). Pesanan berstatus `Batal` dieliminasi dari perhitungan belanja.
- **Entitas Analisis:** Level pembeli unik (`id_pembeli`), mencakup 230 pembeli (229 pembeli dengan username asli + 1 pembeli tanpa username yang dipertahankan sebagai `CUST_012` demi integritas omzet toko).
- **Tanggal Referensi Analisis:** `28 November 2025` (ditetapkan persis 1 hari setelah transaksi terakhir toko pada 27 November 2025).
- **Recency ($R$):** Selisih hari antara tanggal referensi (28 Nov 2025) dengan pesanan selesai terakhir dari pembeli.
- **Frequency ($F$):** Total pesanan unik berstatus selesai yang dilakukan oleh masing-masing pembeli.
- **Monetary ($M$):** Akumulasi nilai `total_pembayaran_rp` dari seluruh pesanan unik selesai yang dilakukan pembeli (satuan Rupiah penuh, mencakup ongkir netto yang dibayar pembeli).

---

## 2. Statistik Deskriptif & Karakteristik Distribusi

| Metrik Statistik | Recency (Hari) | Frequency (Pesanan) | Monetary (Rupiah) |
|:---|:---:|:---:|:---:|
| **Jumlah Sampel ($N$)** | 230 | 230 | 230 |
| **Rata-rata (*Mean*)** | 243,66 hari | 1,13 pesanan | Rp146.356,5 |
| **Standar Deviasi** | 137,99 hari | 0,52 | Rp142.683,4 |
| **Minimum** | 0 hari (kemarin) | 1 pesanan | Rp0 (retur penuh) |
| **Kuartil Bawah ($Q_1$ / 25%)** | 123,25 hari | 1,00 pesanan | Rp79.075,0 |
| **Median ($Q_2$ / 50%)** | 262,00 hari | 1,00 pesanan | Rp97.000,0 |
| **Kuartil Atas ($Q_3$ / 75%)** | 353,50 hari | 1,00 pesanan | Rp175.116,0 |
| **Maksimum** | 505 hari (~16 bulan) | 6 pesanan | Rp1.419.219,0 |
| **Kemiringan (*Skewness*)** | **+0,16** (Hampir Simetris) | **+5,59** (Sangat Miring Kanan) | **+4,60** (Sangat Miring Kanan) |

---

## 3. Analisis Pola Distribusi Per Dimensi

### A. Dimensi Frequency ($F$): Fenomena Single-Buyer Dominan
- **Konsentrasi Ekstrem:** Sebanyak **209 dari 230 pembeli (90,87%) hanya bertransaksi 1 kali**.
- **Distribusi Pembelian Berulang:**
  - 1 kali beli: 209 pembeli (90,87%)
  - 2 kali beli: 15 pembeli (6,52%)
  - 3 kali beli: 4 pembeli (1,74%)
  - 4 kali beli: 1 pembeli (0,43%)
  - 6 kali beli: 1 pembeli (0,43%)
- **Dampak Kritis:** Nilai $Q_1$ dan $Q_3$ bernilai sama persis (1,0), sehingga rentang antar-kuartil $IQR = 0$. Akibatnya, metode pembagian kuantil standar (`qcut`) pada $F$ dipastikan gagal/tumpang-tindih, dan harus digantikan oleh skoring berbasis ambang batas manual pada Minggu 3.

### B. Dimensi Monetary ($M$): Belanja Ritel vs Grosir
- Median nilai belanja adalah **Rp97.000**, mencerminkan pembelian pempek paket reguler (10–20 pcs).
- Rata-rata belanja (Rp146.356) jauh lebih tinggi daripada median karena ditarik oleh sebagian kecil pembeli dengan nilai belanja besar hingga Rp1.419.219.
- Distribusi menunjukkan *positive skewness* yang sangat kuat (+4,60), mengindikasikan perlunya transformasi data (seperti `log1p`) sebelum diaplikasikan pada algoritma berbasis jarak seperti K-Means di Minggu 4.

### C. Dimensi Recency ($R$): Sebaran Waktu Merata
- Recency tersebar luas dari 0 hingga 505 hari dengan kemiringan yang sangat rendah (+0,16).
- Ini menunjukkan bahwa toko mengalami penambahan pembeli baru secara bertahap selama rentang 16 bulan pengamatan.

---

## 4. Analisis Korelasi Antar-Fitur

### Matriks Korelasi Pearson vs Spearman (Rank)

| Pasangan Fitur | Pearson ($r$) | Spearman ($\rho$) | Interpretasi Hubungan |
|:---|:---:|:---:|:---|
| **Frequency vs Monetary** | **+0,58** | **+0,35** | Korelasi positif sedang-kuat. Semakin sering pembeli bertransaksi, total nilai belanja yang diakumulasikan semakin tinggi. |
| **Recency vs Frequency** | **+0,01** | **+0,00** | Tidak terdapat korelasi linear maupun monotonik. Pembeli berulang tersebar di berbagai periode waktu. |
| **Recency vs Monetary** | **+0,01** | **-0,04** | Tidak berkorelasi. Nilai nominal belanja tidak bergantung pada kapan terakhir kali pembeli melakukan transaksi. |

---

## 5. Identifikasi & Penandaan Outlier (Metode IQR 1,5 $\times$ IQR)
Sesuai batasan pengerjaan [Readme.md](file:///c:/Users/ACER/Documents/RSI%20PROJECT/Readme.md), **outlier tidak boleh dihapus**, melainkan ditandai untuk menjaga integritas data pelanggan bernilai tinggi:

1. **Outlier Recency:** **0 pembeli (0%)**. Batas $[-222, 698]$ hari mencakup seluruh rentang data aktual (0 - 505 hari).
2. **Outlier Frequency:** **21 pembeli (9,13%)**. Karena $IQR=0$, seluruh pembeli yang bertransaksi $\ge 2$ kali secara teknis matematika IQR terdeteksi sebagai outlier. Dalam konteks bisnis, kelompok ini adalah **pelanggan setia (*repeat customers*)** yang paling berharga.
3. **Outlier Monetary:** **20 pembeli (8,70%)**. Batas atas $Q_3 + 1,5 \times IQR$ adalah **Rp319.177,5**. Pembeli dengan total belanja di atas batas ini (hingga Rp1.419.219) merupakan segmen pembeli partai besar/grosir (*high-spenders*).
4. **Total Outlier Unik (Salah Satu Dimensi):** **33 pembeli (14,35%)**. Seluruh outlier telah ditandai pada kolom flag `is_outlier_any` di `rfm_table.csv`.

---

## 6. Rekomendasi Teknis untuk Minggu 3 & Minggu 4
1. **Untuk Minggu 3 (Skoring Aturan):** 
   - Gunakan `pd.qcut` dengan `duplicates='drop'` untuk Recency dan Monetary.
   - Gunakan aturan diskrit manual untuk Frequency: Skor 1 untuk $F=1$, Skor 3 untuk $F=2$, dan Skor 5 untuk $F \ge 3$.
2. **Untuk Minggu 4 (K-Means Clustering):**
   - Wajib menerapkan transformasi logaritmik `np.log1p()` pada fitur Monetary dan Frequency guna meredam kemiringan distribusi (*skewness*) sebelum standardisasi (*StandardScaler*).
