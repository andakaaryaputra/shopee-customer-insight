# Laporan Akhir Analisis RFM & K-Means: Segmentasi Pelanggan dan Pola Transaksi Toko Pempek Al-Kindi (Shopee)

**Penyusun:** Tim Data Analytics  
**Periode Data:** 10 Juli 2024 – 27 November 2025 (~16 Bulan)  
**Entitas Analisis:** Transaksi Toko Shopee Seller (Produk Pempek)  
**File Kode Sumber:** `analisis_rfm_kmeans.ipynb`  
**Dataset Utama:** `data_bersih.csv`, `rfm_table.csv`, `rfm_scored.csv`, `rfm_kmeans_results.csv`  

---

## 1. Latar Belakang dan Tujuan Analisis

Toko Pempek Al-Kindi merupakan pelaku usaha mikro, kecil, dan menengah (UMKM) kuliner khas Palembang yang memasarkan produk makanan beku (*frozen food*) melalui platform Shopee. Dalam mengelola strategi pemasaran dan retensi pelanggan, manajemen toko memerlukan pemahaman berbasis data mengenai struktur basis pembeli, loyalitas, dan dinamika transaksi.

Tujuan utama dari proyek analisis 6 minggu ini adalah:
1. Membersihkan dan menstandardisasi data transaksi ekspor Shopee Seller hingga siap dianalisis secara akurat dan bebas dari bias duplikasi nilai uang.
2. Membangun model segmentasi pelanggan menggunakan dua pendekatan komparatif:
   - **Segmentasi Berbasis Aturan (*Rule-Based Scoring*):** Sebagai fondasi acuan (*baseline*) yang transparan.
   - **Segmentasi Berbasis Data (*K-Means Clustering*):** Menggunakan teknik pembelajaran mesin tanpa pengawasan (*unsupervised machine learning*).
3. Mengidentifikasi pola transaksi mencakup preferensi produk, tren waktu, sebaran wilayah geografis, opsi pembayaran, serta bedah khusus alasan pembatalan pesanan.
4. Menyusun rekomendasi bisnis terukur yang diberi label sebagai **hipotesis untuk diuji** guna meningkatkan konversi dan menekan kehilangan pendapatan.

---

## 2. Metodologi Data dan Pembersihan

### A. Karakteristik Data Mentah
File sumber `Shopee Seller Transaction.csv` memuat **403 baris dan 49 kolom**. Sesuai desain sistem Shopee, granularitas data berada pada tingkat item produk dalam pesanan, bukan tingkat pesanan utuh. Terdapat **325 nomor pesanan unik** (`No. Pesanan`) dengan rentang tanggal transaksi dari **10 Juli 2024 hingga 27 November 2025**.

### B. Tindakan Pembersihan & Standardisasi Data (Minggu 1)
1. **Konversi Mata Uang Rupiah:** Seluruh kolom moneter diekspor oleh platform Shopee menggunakan tanda titik sebagai pemisah ribuan (contoh: `"134.000"`). Tanda titik dihilangkan dan dikonversi menjadi tipe numerik `float64` dalam satuan Rupiah penuh (`134000.0`).
2. **Pencegahan Penggandaan Nilai Moneter:** Kolom `Total Pembayaran` mencatat nilai tagihan pesanan utuh yang terulang pada setiap item dalam pesanan multi-item. Data diagregasi ke level nomor pesanan unik (`id_pesanan`) dengan mengambil nilai pembayaran tepat satu kali (`first`).
3. **Pemisahan Status Transaksi:** Dari 325 pesanan unik, 261 pesanan berstatus `Selesai` dan 64 pesanan berstatus `Batal`. Sesuai batasan analisis, pesanan berstatus `Batal` dipisahkan sepenuhnya dari perhitungan RFM dan dianalisis terpisah pada analisis pembatalan.
4. **Perlindungan Privasi (PII):** Seluruh data identitas pribadi pembeli (`Nama Penerima`, `No. Telepon`, `Alamat Pengiriman`, dan catatan pesanan) dibuang. Nilai `Username (Pembeli)` digantikan dengan kode acak anonim (`CUST_001` s.d. `CUST_265`). Sebanyak 1 transaksi selesai tanpa username dipertahankan dengan identifier pengganti agar integritas omzet toko tetap utuh.
5. **Eliminasi Kolom Konstan:** Kolom tanpa informasi pembeda (`SKU Induk`, `Diskon Dari Shopee`, `Cashback Koin`, `Paket Diskon`, dll.) dieliminasi.

---

## 3. Feature Engineering RFM dan Karakteristik Distribusi (Minggu 2)

Perhitungan metrik RFM dilakukan pada level pembeli unik (`id_pembeli`) yang bertransaksi pada pesanan selesai ($N = 230$ pembeli, omzet Rp33.661.986).

### A. Definisi Operasional Fitur RFM
- **Tanggal Referensi:** `28 November 2025` (ditetapkan persis 1 hari setelah transaksi terakhir toko).
- **Recency ($R$):** Selisih hari antara tanggal referensi dengan pesanan selesai terakhir pembeli.
- **Frequency ($F$):** Total pesanan unik berstatus selesai per pembeli.
- **Monetary ($M$):** Akumulasi total pembayaran pesanan unik selesai per pembeli (satuan Rupiah).

### B. Karakteristik Distribusi dan Kemiringan (*Skewness*)

| Metrik Statistik | Recency ($R$, Hari) | Frequency ($F$, Pesanan) | Monetary ($M$, Rupiah) |
|:---|:---:|:---:|:---:|
| **Rata-rata (*Mean*)** | 243,66 hari | 1,13 pesanan | Rp146.356,5 |
| **Standar Deviasi** | 137,99 hari | 0,52 | Rp142.683,4 |
| **Kuartil Bawah ($Q_1$)** | 123,25 hari | 1,00 pesanan | Rp79.075,0 |
| **Median ($Q_2$)** | 262,00 hari | 1,00 pesanan | Rp97.000,0 |
| **Kuartil Atas ($Q_3$)** | 353,50 hari | 1,00 pesanan | Rp175.116,0 |
| **Maksimum** | 505 hari | 6 pesanan | Rp1.419.219,0 |
| **Kemiringan (*Skewness*)** | **+0,16** (Simetris) | **+5,59** (Sangat Miring Kanan) | **+4,60** (Sangat Miring Kanan) |

### C. Temuan Kritis Dimensi Frequency
Sebanyak **209 dari 230 pembeli (90,87%) hanya membeli satu kali ($F=1$)**. Hanya 21 pembeli yang pernah melakukan pembelian berulang ($F \ge 2$). Akibatnya, nilai rentang antar-kuartil $IQR = Q_3 - Q_1 = 0$, sehingga pembagian kuantil standar pada $F$ dipastikan gagal dan wajib diganti dengan skoring manual terjustifikasi.

### D. Perlakuan Outlier (Metode IQR)
Terdeteksi 21 outlier pada Frequency ($F \ge 2$) dan 20 outlier pada Monetary ($M > \text{Rp}319.177,5$). Sesuai batasan analisis, **seluruh outlier tidak dihapus** melainkan hanya diberi flag penanda, karena kelompok ini merepresentasikan pelanggan setia dan pembeli partai besar yang krusial bagi bisnis.

---

## 4. Hasil Segmentasi: Perbandingan Aturan Baseline vs K-Means

### A. Segmentasi Berbasis Aturan Baseline (Minggu 3)
Skor $R$ dan $M$ dibagi menjadi 5 kuintil (`pd.qcut` dengan `duplicates='drop'`). Skor $F$ dibagi menggunakan ambang batas manual: Skor 1 ($F=1$), Skor 3 ($F=2$), dan Skor 5 ($F \ge 3$). Ditetapkan 5 segmen aturan:

| Segmen Aturan | Logika Aturan | Jumlah Pembeli | Proporsi (%) | Rata-rata Recency | Rata-rata Monetary | Kontribusi Omzet (%) |
|:---|:---|:---:|:---:|:---:|:---:|:---:|
| **Berisiko (*At Risk*)** | $F=1, R \in [2,3]$ | 89 | 38,70% | 286,7 hari | Rp117.516 | **31,07%** |
| **Pembeli Potensial** | $F=1, R \in [4,5], M \ge 3$ | 43 | 18,70% | 95,2 hari | Rp192.924 | **24,64%** |
| **Tidak Aktif (*Lost*)** | $F=1, R = 1$ | 39 | 16,96% | 445,9 hari | Rp130.856 | **15,16%** |
| **Pembeli Baru** | $F=1, R \in [4,5], M \le 2$ | 38 | 16,52% | 102,5 hari | Rp76.825 | **8,67%** |
| **Pelanggan Loyal** | $F \ge 2$ | 21 | 9,13% | 245,3 hari | Rp327.839 | **20,45%** |

### B. Segmentasi Berbasis Data K-Means (Minggu 4)
Fitur $F$ dan $M$ ditransformasikan dengan $\ln(x+1)$ lalu distandarisasi bersama $R$ menggunakan *StandardScaler*. Algoritma dijalankan untuk rentang $k=2..6$ (`n_init=10`, `random_state=42`).

**Evaluasi Pemilihan Nilai $k$:**
- **$k=2$:** Inersia 480,06; Silhouette 0,5798; Davies-Bouldin 0,8273. Hanya membelah $F=1$ ($N=209$) vs $F \ge 2$ ($N=21$).
- **$k=3$ (Terpilih):** Inersia 323,86; **Silhouette 0,4485**; **Davies-Bouldin 0,8099**. Seluruh klaster memenuhi syarat ukuran sampel ($> 5\%$). Uji stabilitas 10 random seeds menghasilkan **Mean ARI = 0,9984** (sangat stabil).
- **$k \ge 4$:** Ditolak karena menghasilkan klaster degenerasi anomali beranggotakan hanya **1 pembeli (0,43%)**, melanggar batas kelayakan metodologis.

### C. Profil Tiga Klaster K-Means Terpilih ($k=3$)

| Parameter Klaster | Klaster 0: *Pembeli Baru & Potensial* | Klaster 1: *Pelanggan Loyal (Repeat)* | Klaster 2: *Pembeli Lama / Berisiko* |
|:---|:---:|:---:|:---:|
| **Jumlah Anggota ($N$)** | **95 pembeli** (41,30%) | **21 pembeli** (9,13%) | **114 pembeli** (49,57%) |
| **Rata-rata Recency** | 117,9 hari (~3,9 bulan) | 245,3 hari (~8,2 bulan) | 348,2 hari (~11,6 bulan) |
| **Rata-rata Frequency** | 1,00 order | **2,48 order** | 1,00 order |
| **Rata-rata Belanja (Rp)** | **Rp155.086** | **Rp327.839** | **Rp105.651** |
| **Akumulasi Omzet (Rp)** | **Rp14.733.162** | **Rp6.884.610** | **Rp12.044.214** |
| **Pangsa Omzet Toko** | **43,77%** | **20,45%** | **35,78%** |

### D. Perbandingan Antara K-Means dan Segmen Aturan
Tingkat kesepakatan partisi antara K-Means $k=3$ dan segmen aturan baseline menghasilkan **Adjusted Rand Index (ARI) = 0,4439**. K-Means memisahkan 21 pelanggan loyal ke klaster tersendiri (100% konsisten), sementara 209 pembeli tunggal dipartisi menjadi dua kelompok berbasis kombinasi kebaruan transaksi (*Recency*) dan daya beli (*Monetary*).

---

## 5. Ringkasan Pola Transaksi Deskriptif (Minggu 5)

1. **Preferensi Varian Produk:**
   - **Pempek Mini 40 pcs (Lenjer, Kulit & Telur):** Produk terlaris mutlak, terjual **117 kali (36,4%)**. Produk ini menjadi penggerak utama nilai belanja tinggi di Klaster 0 (72 pesanan).
   - **Pempek Mini 20 pcs:** Terjual **68 kali (21,2%)**, menjadi varian favorit pelanggan berulang di Klaster 1 (15 pesanan).
   - Keranjang belanja sangat terkonsentrasi dengan rata-rata **1,23 item per pesanan**.
2. **Pola Waktu Transaksi:**
   - **Musiman Bulanan:** Lonjakan tertinggi terjadi pada **Maret 2025 (39 pesanan)** menjelang Hari Raya Idul Fitri dan **Juli 2025 (38 pesanan)** pada kampanye promo Shopee 7.7. Titik terendah terjadi pada Januari (4 pesanan) dan April (2 pesanan).
   - **Hari Belanja:** Paling aktif pada awal pekan (**Selasa: 47 pesanan, Senin: 42 pesanan**).
   - **Jam Transaksi:** Memuncak pada waktu istirahat kerja siang hari (12:00–14:00) dan malam hari (19:00–21:00).
3. **Pola Wilayah Geografis:**
   - Menjangkau pembeli di **28 provinsi**. Konsentrasi pesanan tertinggi berada di **Jawa Barat (25,3%)**, **Jawa Timur (13,4%)**, **Sumatera Selatan (11,5%)**, **Jawa Tengah (9,2%)**, dan **DKI Jakarta (8,8%)**. Lebih dari 56% pesanan dikirimkan ke Pulau Jawa.
4. **Metode Pembayaran dan Pengiriman:**
   - Metode nontunai mendominasi: **Saldo ShopeePay (39,1%)** dan **Online Payment / VA (36,0%)**, sementara metode COD digunakan pada 13,8% pesanan.
   - Pengiriman 100% menggunakan kurir reguler cashless Shopee (Anteraja dan SPX Standard).
5. **Penetrasi Diskon dan Voucher:**
   - Voucher Shopee (terutama gratis ongkir) dimanfaatkan oleh **45,2% pesanan**.
   - Diskon langsung produk dari penjual dimanfaatkan oleh **34,5% pesanan**.
   - **Voucher internal toko hanya tercatat pada 2 pesanan (0,8%)**, menunjukkan peluang promosi internal toko yang belum dimanfaatkan.
6. **Analisis Khusus Pembatalan Pesanan (64 Pesanan Batal / 19,7%):**
   - **23 pesanan (35,9%):** Dibatalkan oleh pembeli untuk mengubah pesanan, alamat, atau voucher.
   - **15 pesanan (23,4%):** Dibatalkan otomatis oleh sistem Shopee karena belum dibayar (*expired*).
   - **15 pesanan (23,4%): Dibatalkan otomatis oleh sistem Shopee karena penjual terlambat mengatur pengiriman.** Ini merupakan kehilangan pendapatan operasional (*lost revenue*) langsung yang dapat dicegah.

---

## 6. Rekomendasi Bisnis Terarah (Diberi Label Hipotesis)

Seluruh rekomendasi berikut dirumuskan secara terukur dan wajib diuji melalui eksperimen terkontrol:

### Hipotesis 1: Konversi Pembeli Baru Menjadi Pelanggan Loyal melalui Voucher Isi Ulang
- **Rasional:** Klaster 0 mencakup 95 pembeli bernilai tinggi yang menyumbang 43,77% omzet namun baru bertransaksi 1 kali paket 40 pcs.
- **Tindakan:** Mengirimkan pesan siaran (*broadcast chat*) Shopee berisi voucher diskon khusus pembelian ulang (*repeat order voucher*) sebesar 10% untuk paket isi ulang 20/40 pcs dalam rentang 30–45 hari pasca-transaksi pertama.
- **Cara Menguji:** Terapkan uji A/B (*A/B Testing*) dengan membagi Klaster 0 menjadi kelompok perlakuan (menerima broadcast voucher) dan kelompok kontrol (tanpa broadcast). Ukur tingkat pembelian ulang (*repurchase rate*) dalam waktu 60 hari.

### Hipotesis 2: Pemulihan Omzet Operasional yang Hilang Melalui Pengetatan SLA Pengiriman
- **Rasional:** Sebanyak 15 pesanan batal murni karena keterlambatan toko memproses resi pengiriman tepat waktu.
- **Tindakan:** Menerapkan SOP pemrosesan pesanan maksimal 24 jam dengan mengaktifkan pengingat notifikasi harian pada pukul 10:00 dan 15:00 WIB.
- **Cara Menguji:** Bandingkan persentase pesanan batal akibat alasan keterlambatan pengiriman selama periode 3 bulan sebelum dan sesudah penerapan SOP. Hipotesis diterima jika pembatalan operasional turun minimal 80%.

### Hipotesis 3: Aktivasi Fitur Voucher Toko (Follower Voucher) untuk Mendorong Pembelian Keranjang Ganda
- **Rasional:** Penggunaan voucher penjual saat ini hanya 0,8%, sementara 80,5% pesanan hanya membeli 1 item produk (rata-rata 1,23 item/pesanan).
- **Tindakan:** Membuat voucher toko bertingkat (*Tiered Voucher*), misalnya "Diskon Rp10.000 dengan minimal belanja Rp150.000" untuk mendorong pembelian varian pelengkap (seperti pempek kulit atau cuko tambahan).
- **Cara Menguji:** Pantau kenaikan rata-rata item per pesanan (*basket size*) dan persentase pesanan multi-item selama 60 hari masa promosi dibandingkan data historis.

---

## 7. Keterbatasan Penelitian (*Limitations*)

Sesuai standar objektivitas analitik, batasan-batasan berikut wajib diperhatikan:
1. **Dominasi Pembelian Tunggal (Frequency Lemah):** Sebanyak 90,87% pembeli hanya bertransaksi satu kali ($F=1$). Akibatnya, dimensi Frequency memiliki daya pembeda yang rendah, dan pemisahan klaster K-Means pada pembeli tunggal murni ditentukan oleh interaksi Recency dan Monetary.
2. **Ukuran Sampel Terbatas:** Analisis didasarkan pada sampel 230 pembeli unik dari satu toko tunggal (*single merchant*) dengan kategori produk spesifik (pempek Palembang beku), sehingga temuan tidak dapat digeneralisasi untuk toko atau kategori produk lain di e-commerce.
3. **Periode Pengamatan:** Rentang waktu 16 bulan mencakup hanya satu siklus penuh hari raya keagamaan, sehingga pola musiman (seperti lonjakan di bulan Maret dan Juli) bersifat indikasi awal dan belum terbukti sebagai siklus tahunan permanen.
4. **Cakupan Kanal Penjualan:** Data transaksi hanya mencakup penjualan melalui kanal Shopee dan tidak memperhitungkan transaksi pembeli di luar platform (misalnya WhatsApp, Instagram, atau penjualan offline).
5. **Sifat Hubungan Data:** Seluruh temuan bersifat **deskriptif dan asosiatif**, bukan hubungan sebab-akibat (*causality*).
