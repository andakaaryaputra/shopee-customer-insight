# Profil Segmen K-Means dan Analisis Pola Transaksi (Minggu 5)

**Tanggal Penyusunan:** 18 November 2026  
**File Sumber:** `Shopee Seller Transaction.csv`, `data_bersih.csv`, `rfm_kmeans_results.csv`  
**Notebook:** `analisis_rfm_kmeans.ipynb` (Bagian Minggu 5)  

---

## 1. Profil Komprehensif Klaster K-Means ($k=3$)

Berdasarkan hasil pemodelan K-Means pada Minggu 4, pembeli terkelompok ke dalam 3 klaster alami yang diberi nama dan deskripsi deskriptif murni berdasarkan bukti data matematis:

| Parameter Profil | Klaster 0: *Pembeli Baru & Potensial* | Klaster 1: *Pelanggan Loyal (Repeat)* | Klaster 2: *Pembeli Lama / Berisiko* | Total Keseluruhan |
|:---|:---:|:---:|:---:|:---:|
| **Jumlah Pembeli ($N$)** | **95 pembeli** (41,30%) | **21 pembeli** (9,13%) | **114 pembeli** (49,57%) | **230 pembeli** (100%) |
| **Status Ukuran Sampel** | Aman (> 5%) | Aman (> 5%) | Aman (> 5%) | Valid |
| **Rata-rata Recency** | **117,9 hari** (~3,9 bulan) | **245,3 hari** (~8,2 bulan) | **348,2 hari** (~11,6 bulan) | **243,7 hari** |
| **Median Recency** | 114,0 hari | 262,0 hari | 353,5 hari | 262,0 hari |
| **Rata-rata Frequency** | **1,00 pesanan** | **2,48 pesanan** | **1,00 pesanan** | **1,13 pesanan** |
| **Maksimum Frequency** | 1 pesanan | 6 pesanan | 1 pesanan | 6 pesanan |
| **Rata-rata Belanja (Rp)** | **Rp155.086** | **Rp327.839** | **Rp105.651** | **Rp146.356** |
| **Median Belanja (Rp)** | Rp97.000 | Rp222.000 | Rp92.000 | Rp97.000 |
| **Total Akumulasi Belanja** | **Rp14.733.162** | **Rp6.884.610** | **Rp12.044.214** | **Rp33.661.986** |
| **Kontribusi Omzet (%)** | **43,77%** | **20,45%** | **35,78%** | **100,00%** |

### Deskripsi Deskriptif Klaster:
1. **Klaster 0 (*Pembeli Baru & Potensial*):** Pembeli tunggal ($F=1$) yang bertransaksi baru-baru ini ($\le 4$ bulan terakhir) dengan rata-rata belanja tertinggi kedua (Rp155.086) dan merupakan kontributor omzet terbesar toko (43,77%).
2. **Klaster 1 (*Pelanggan Loyal*):** Kelompok pembeli berulang ($F \ge 2$) yang mencakup 9,13% pembeli namun menyumbang lebih dari 20% omzet dengan rata-rata belanja tertinggi (Rp327.839).
3. **Klaster 2 (*Pembeli Lama / Berisiko*):** Pembeli tunggal ($F=1$) dari periode lebih dari 11 bulan lalu dengan nilai belanja rata-rata terendah (Rp105.651) yang belum pernah kembali lagi ke toko.

---

## 2. Eksplorasi Pola Transaksi Deskriptif (Pesanan Selesai)

### A. Pola Produk dan Varian Terlaris
Dari total 321 baris item produk pada pesanan Selesai:
1. **Pempek Mini 40 pcs (Lenjer, Kulit & Telur):** Terjual **117 kali** (36,4%). Varian ini mendominasi Klaster 0 (72 kali) dan Klaster 2 (35 kali).
2. **Pempek Mini 20 pcs (Lenjer, Kulit & Telur):** Terjual **68 kali** (21,2%). Varian ini paling banyak dipesan oleh pelanggan berulang di Klaster 1 (15 kali).
3. **Pempek Medium 10 pcs:** Terjual **24 kali** (7,5%).
4. **Pempek Tenggiri Premium 20 pcs:** Terjual **21 kali** (6,5%).
5. **Rata-rata Item per Pesanan:** **1,23 item/pesanan** (210 pesanan terdiri dari 1 item, 43 pesanan terdiri dari 2 item, 7 pesanan 3 item, dan 1 pesanan 4 item).

### B. Pola Waktu Transaksi (Musiman, Hari, dan Jam)
- **Tren Bulanan:** 
  - Penjualan menunjukkan dua lonjakan volume transaksi yang mencolok: **Maret 2025 (39 pesanan)** bertepatan dengan momentum bulan Ramadan / persiapan Idul Fitri, dan **Juli 2025 (38 pesanan)** bertepatan dengan masa promo pertengahan tahun Shopee (7.7).
  - Volume transaksi terendah tercatat pada **Januari 2025 (4 pesanan)** dan **April 2025 (2 pesanan)** pasca-Lebaran.
- **Pola Hari Belanja:**
  - Hari dengan transaksi tertinggi adalah **Selasa (47 pesanan)** dan **Senin (42 pesanan)**.
  - Hari dengan transaksi terendah adalah **Jumat (30 pesanan)** dan **Rabu (33 pesanan)**.
- **Pola Jam Transaksi:**
  - Aktivitas belanja memuncak pada siang hari pukul **12:00 – 14:00 WIB** (waktu istirahat kerja) dan malam hari pukul **19:00 – 21:00 WIB**.

### C. Sebaran Geografis Pembeli
Pembeli toko tersebar di **28 provinsi** di Indonesia, dengan konsentrasi wilayah teratas:
1. **Jawa Barat:** 66 pesanan (25,29%)
2. **Jawa Timur:** 35 pesanan (13,41%)
3. **Sumatera Selatan (Lokal):** 30 pesanan (11,49%)
4. **Jawa Tengah:** 24 pesanan (9,20%)
5. **DKI Jakarta:** 23 pesanan (8,81%)
*Catatan:* Lebih dari 56% pembeli berada di Pulau Jawa, menunjukkan bahwa produk pempek beku (*frozen pempek*) berhasil menjangkau pasar antar-pulau dengan opsi pengiriman reguler/cashless.

### D. Metode Pembayaran dan Pengiriman
- **Metode Pembayaran:** 
  - Didominasi oleh pembayaran digital nontunai: **Saldo ShopeePay (102 pesanan / 39,1%)** dan **Online Payment / Virtual Account (94 pesanan / 36,0%)**.
  - Metode **COD (Bayar di Tempat)** digunakan pada **36 pesanan (13,8%)**.
  - Opsi lain meliputi SeaBank Instan (17 pesanan), Kartu Kredit/Debit (7 pesanan), dan gerai retail Indomaret/Alfamart (5 pesanan).
- **Opsi Pengiriman:** 100% pesanan selesai dikirim melalui jalur cashless Shopee, didominasi oleh layanan **Anteraja Reguler** dan **SPX Standard**.

### E. Penetrasi Diskon, Voucher, dan Koin Shopee
- **Voucher Shopee:** Digunakan pada **118 dari 261 pesanan (45,2%)**, terutama voucher gratis ongkos kirim.
- **Diskon dari Penjual:** Dinikmati oleh **90 pesanan (34,5%)** melalui potongan harga langsung produk.
- **Potongan Koin Shopee:** Dimanfaatkan oleh **23 pesanan (8,8%)**.
- **Voucher Toko/Penjual:** Hanya tercatat **2 pesanan (0,8%)**, mengindikasikan bahwa fitur voucher internal toko belum dioptimalkan oleh penjual.

---

## 3. Analisis Khusus Pembatalan Pesanan (*Order Cancellation Analysis*)
Dari 325 nomor pesanan unik yang masuk, terdapat **64 pesanan (19,69%) yang dibatalkan** (mencakup 82 baris item produk). 

| Kategori Utama Pembatalan | Jumlah Pesanan | Proporsi (%) | Keterangan Rinci |
|:---|:---:|:---:|:---|
| **Pembeli: Ubah Pesanan / Alamat** | **23** | **35,94%** | Pembeli membatalkan pesanan untuk mengubah varian pempek, alamat pengiriman, atau mengganti voucher. |
| **Sistem: Pesanan Belum Dibayar** | **15** | **23,44%** | Pembeli memilih metode transfer/gerai namun melewati batas waktu pembayaran (*expired payment*). |
| **Sistem: Penjual Terlambat Atur Pengiriman** | **15** | **23,44%** | Dibatalkan otomatis oleh sistem Shopee karena penjual tidak memproses pesanan tepat waktu. |
| **Pembeli: Berubah Pikiran / Alasan Lain** | **7** | **10,94%** | Pembatalan sepihak oleh pembeli tanpa perubahan pesanan baru. |
| **Sistem / Logistik: Pengiriman Gagal** | **2** | **3,12%** | Masalah operasional logistik kurir di lapangan. |
| **Penjual: Stok Produk Habis** | **1** | **1,56%** | Pembatalan inisiatif toko karena kehabisan stok. |
| **Pembeli: Kesulitan Proses Bayar** | **1** | **1,56%** | Kendala teknis pembayaran di sisi pembeli. |
| **Total Pembatalan** | **64** | **100,00%** | **19,69% dari total 325 pesanan masuk** |

> **Poin Evaluasi Kritis Toko:** Terdapat **15 pesanan (23,44% dari total pembatalan)** yang batal murni akibat operasional internal toko (keterlambatan mengatur resi pengiriman). Ini merupakan potensi omzet yang hilang (*lost revenue*) yang dapat dicegah dengan perbaikan operasional SOP pengiriman.

---

## 4. Tiga Pertanyaan Lanjutan yang Dapat Dijawab Data Ini
1. **Konversi Ulang Pembeli Potensial:** Apakah 95 pembeli pada Klaster 0 (*Pembeli Baru & Potensial*) yang membeli paket 40 pcs memiliki kecenderungan membeli ulang jika diberikan penawaran paket isi ulang dalam rentang waktu 30-60 hari?
2. **Mitigasi Pembatalan Operasional:** Berapa potensi omzet yang dapat diselamatkan jika toko menerapkan waktu respons pesanan maksimal 24 jam untuk mencegah 15 pesanan batal otomatis akibat batas waktu pengiriman?
3. **Efektivitas Voucher Toko:** Mengapa penggunaan voucher penjual hanya 0,8% (2 pesanan), dan apakah pembuatan voucher khusus pengikut toko (*Follower Voucher*) dapat mendorong pembelian ulang pada 21 pelanggan loyal?
