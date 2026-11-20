# Aturan dan Dokumentasi Segmentasi RFM Berbasis Aturan (Minggu 3)

**Tanggal Penyusunan:** 18 November 2026  
**File Sumber:** `rfm_table.csv`  
**File Hasil:** `rfm_scored.csv`  
**Notebook:** `analisis_rfm_kmeans.ipynb` (Bagian Minggu 3)  

---

## 1. Landasan Metodologi Skoring

Sesuai panduan pengerjaan di [Readme.md](file:///c:/Users/ACER/Documents/RSI%20PROJECT/Readme.md), segmentasi berbasis aturan dibuat sebelum pemodelan K-Means untuk berfungsi sebagai **fondasi acuan (*baseline*)** yang transparan, mudah diinterpretasikan oleh manajemen bisnis, dan bebas dari bias penyesuaian pasca-eksekusi (*p-hacking*).

### A. Skoring Recency ($R$) & Monetary ($M$) Menggunakan Kuantil (`pd.qcut`)
Karena nilai $R$ dan $M$ memiliki variansi yang kontinu, pembagian skor 1 sampai 5 menggunakan kuantil 5 bagian (quintile / 20-persentil) dengan parameter `duplicates='drop'`:
- **Recency ($R$):** Semakin kecil hari (semakin baru transaksi), semakin tinggi skornya.
  - Skor 5 (Sangat Baru): $\le 113,6$ hari (0 s.d. ~3,7 bulan) [46 pembeli]
  - Skor 4 (Baru): $> 113,6$ s.d. $188,0$ hari (~3,7 s.d. 6,2 bulan) [46 pembeli]
  - Skor 3 (Sedang): $> 188,0$ s.d. $272,0$ hari (~6,2 s.d. 9,0 bulan) [49 pembeli]
  - Skor 2 (Lama): $> 272,0$ s.d. $387,0$ hari (~9,0 s.d. 12,9 bulan) [45 pembeli]
  - Skor 1 (Sangat Lama): $> 387,0$ s.d. $505,0$ hari (~12,9 s.d. 16,8 bulan) [44 pembeli]
- **Monetary ($M$):** Semakin besar akumulasi belanja, semakin tinggi skornya.
  - Skor 1 (Sangat Rendah): $\le \text{Rp}77.357$ [46 pembeli]
  - Skor 2 (Rendah): $> \text{Rp}77.357$ s.d. $\text{Rp}89.911$ [48 pembeli]
  - Skor 3 (Sedang): $> \text{Rp}89.911$ s.d. $\text{Rp}103.384$ [44 pembeli]
  - Skor 4 (Tinggi): $> \text{Rp}103.384$ s.d. $\text{Rp}199.929$ [46 pembeli]
  - Skor 5 (Sangat Tinggi): $> \text{Rp}199.929$ s.d. $\text{Rp}1.419.219$ [46 pembeli]

### B. Skoring Frequency ($F$) Menggunakan Ambang Batas Diskrit Manual
Pada Minggu 2 ditemukan bahwa **90,87% pembeli hanya bertransaksi 1 kali ($IQR=0$)**, sehingga `pd.qcut` dipastikan mengalami batas tumpang-tindih (*overlapping bin edges*). Oleh karena itu, skor $F$ ditetapkan secara manual dengan justifikasi empiris:
- **Skor 1 (Pembeli Sekali / Single-Buyer):** $F = 1$ pesanan (209 pembeli, 90,87%).
- **Skor 3 (Pembeli Mengulang / Repeat Buyer):** $F = 2$ pesanan (15 pembeli, 6,52%).
- **Skor 5 (Pembeli Sangat Sering / Frequent Buyer):** $F \ge 3$ pesanan (6 pembeli, 2,61%).

---

## 2. Definisi Logika Aturan Segmen (*Rule-Based Segmentation*)

Segmentasi dirancang secara tegas dan deterministik (*mutually exclusive & collectively exhaustive*), menjamin setiap pembeli masuk ke tepat satu kelompok:

| No | Nama Segmen | Logika Aturan Penetapan | Rasional / Justifikasi Bisnis |
|:---:|:---|:---|:---|
| 1 | **Pelanggan Loyal** | $F \ge 2$ | Kelompok langka (9,13%) yang terbukti melakukan pembelian ulang pempek lebih dari 1 kali. Menjadi aset retensi terpenting toko. |
| 2 | **Pembeli Potensial** | $F = 1 \text{ DAN } R \in \{4, 5\} \text{ DAN } M \ge 3$ | Pembeli baru dalam 6 bulan terakhir dengan nilai belanja menengah ke atas ($> \text{Rp}89.911$). Paling berpeluang dikonversi menjadi pelanggan loyal. |
| 3 | **Pembeli Baru** | $F = 1 \text{ DAN } R \in \{4, 5\} \text{ DAN } M \le 2$ | Pembeli baru dalam 6 bulan terakhir namun dengan nominal transaksi pempek paket kecil/percobaan ($\le \text{Rp}89.911$). |
| 4 | **Berisiko (*At Risk*)** | $F = 1 \text{ DAN } R \in \{2, 3\}$ | Pembeli yang bertransaksi 6 hingga 12 bulan lalu dan belum pernah membeli ulang. Memiliki risiko tinggi churn jika tidak segera diaktivasi. |
| 5 | **Tidak Aktif (*Lost*)** | $F = 1 \text{ DAN } R = 1$ | Pembeli dari periode awal toko (> 13 bulan lalu) yang tidak pernah kembali lagi. Tingkat churn sangat tinggi. |

---

## 3. Ringkasan Profil & Sebaran Segmen

| Nama Segmen | Jumlah Pembeli | Persentase | Rata-rata Recency | Rata-rata Frequency | Rata-rata Monetary | Total Kontribusi Omzet | % Kontribusi Omzet |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Berisiko (*At Risk*)** | 89 | 38,70% | 286,65 hari | 1,00 pesanan | Rp117.516,0 | Rp10.458.921 | **31,07%** |
| **Pembeli Potensial** | 43 | 18,70% | 95,19 hari | 1,00 pesanan | Rp192.924,2 | Rp8.295.739 | **24,64%** |
| **Tidak Aktif (*Lost*)** | 39 | 16,96% | 445,90 hari | 1,00 pesanan | Rp130.855,9 | Rp5.103.379 | **15,16%** |
| **Pembeli Baru** | 38 | 16,52% | 102,47 hari | 1,00 pesanan | Rp76.824,7 | Rp2.919.337 | **8,67%** |
| **Pelanggan Loyal** | 21 | 9,13% | 245,33 hari | 2,48 pesanan | Rp327.838,6 | Rp6.884.610 | **20,45%** |
| **Total Keseluruhan** | **230** | **100,00%** | **243,66 hari** | **1,13 pesanan** | **Rp146.356,5** | **Rp33.661.986** | **100,00%** |

---

## 4. Evaluasi Ukuran Segmen Sesuai Pedoman
- Sesuai batasan analisis, segmen berukuran **di bawah 5% harus ditandai**.
- Pada skema 5 segmen ini, seluruh segmen memiliki proporsi **di atas 5%** (terkecil adalah *Pelanggan Loyal* dengan 9,13% / 21 pembeli).
- Apabila *Pelanggan Loyal* dipecah lebih lanjut menjadi *Champions* (11 pembeli, 4,78%) dan *Loyal Customers* (10 pembeli, 4,35%), kedua sub-segmen tersebut berada di bawah batas ambang 5% sehingga kurang andal untuk analisis statistik terpisah. Oleh karena itu, penggabungan ke dalam 5 segmen utama terbukti paling kokoh secara metodologis.

---

## 5. Kesiapan Menuju Minggu 4 (K-Means)
Tabel hasil skoring aturan pada `rfm_scored.csv` akan dijadikan variabel pembanding (*ground truth baseline*) pada Minggu 4. Label klaster K-Means nantinya akan diuji tingkat kesepakatannya (*agreement*) terhadap kolom `segmen_aturan` menggunakan *Crosstabulation* dan *Adjusted Rand Index* (ARI).
