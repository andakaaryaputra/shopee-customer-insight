# Log Pembersihan Data Transaksi Shopee (Minggu 1)

**Tanggal Eksekusi:** 18 November 2026  
**File Sumber:** `Shopee Seller Transaction.csv`  
**File Hasil:** `data_bersih.csv`  
**Notebook:** `analisis_rfm_kmeans.ipynb`  

---

## 1. Baseline Data Mentah
- **Ukuran File Mentah:** 403 baris, 49 kolom.
- **Granularitas Baris:** Level item produk dalam pesanan (bukan 1 baris per pesanan).
- **Nomor Pesanan Unik:** 325 nomor pesanan (`No. Pesanan`).
- **Komposisi Status Pesanan:**
  - `Selesai`: 321 baris item (261 nomor pesanan unik).
  - `Batal`: 82 baris item (64 nomor pesanan unik).
  - Tidak terdapat tumpang tindih pesanan antara Selesai dan Batal (261 + 64 = 325 pesanan).
- **Rentang Tanggal Pesanan:** 10 Juli 2024 (14:22:00) s.d. 27 November 2025 (10:14:00) (~16 bulan).

---

## 2. Masalah yang Teridentifikasi & Tindakan Pembersihan

### A. Format Mata Uang (Pemisah Ribuan Titik)
- **Kondisi:** Format kolom uang Shopee diekspor dengan titik sebagai pemisah ribuan (contoh: `"134.000"` untuk Rp134.000). Jika dibaca langsung tanpa konversi, pandas menerjemahkannya sebagai angka pecahan desimal `134.0`.
- **Tindakan:** Membaca CSV dengan tipe data string (`dtype=str`), membersihkan pemisah titik menggunakan `.replace('.', '')`, dan mengubah tipe data menjadi `float64`.
- **Verifikasi:**
  - Nilai pesanan selesai terkecil: Rp0 (pesanan retur disetujui, no pesanan `24120782F49NRK`).
  - Nilai pesanan selesai median: Rp96.900.
  - Nilai pesanan selesai rata-rata: Rp128.973.
  - Nilai pesanan selesai terbesar: Rp1.013.724 (pembelian grosir).
  - Total omzet pesanan selesai: Rp33.661.986.

### B. Penggandaan Nilai Pesanan pada Multi-Item
- **Kondisi:** Kolom `Total Pembayaran` mencatat nilai tagihan satu pesanan utuh, sehingga pada pesanan dengan lebih dari satu item barang, nilai yang sama tercatat berulang pada setiap baris item. Menjumlahkan kolom ini secara langsung akan menggandakan nilai Monetary.
- **Tindakan:** Mengagregasikan data mentah per nomor pesanan (`id_pesanan`) dan mengambil nilai `Total Pembayaran` tepat satu kali (`first`).
- **Hasil:** Nilai moneter pesanan terkonsolidasi dengan benar tanpa risiko bias pembengkakan nilai belanja.

### C. Penanganan Nilai Hilang (Missing Values) & Karakter Simbol
- **Kondisi 1 (`Waktu Pembayaran Dilakukan`):** Terdapat 36 baris dengan karakter `"-"` yang menandakan pesanan belum dibayar (pada pesanan berstatus Batal).
- **Tindakan 1:** Mengganti karakter `"-"` dengan `NaN` sebelum konversi ke format datetime. Pada pesanan Selesai, seluruh baris memiliki tanggal pembayaran yang valid (0 missing).
- **Kondisi 2 (`Username (Pembeli)`):** Terdapat 1 baris pesanan Selesai (`2412173UU0147H`) yang memiliki nilai `Username (Pembeli)` berupa `NaN`.
- **Tindakan 2:** Baris transaksi ini tetap dipertahankan agar jumlah pesanan Selesai tidak berkurang dari 261 pesanan. Username yang hilang diisi dengan identifier sementara `UNKNOWN_BUYER_01` sebelum dilakukan mapping ID pembeli.

### D. Perlindungan Privasi Data (PII)
- **Kondisi:** File mentah memuat data pribadi pembeli (`Nama Penerima`, `No. Telepon`, `Alamat Pengiriman`, `Catatan dari Pembeli`, `Catatan`).
- **Tindakan:**
  - Seluruh kolom PII di atas dihapus secara permanen dari dataset olahan.
  - Nilai `Username (Pembeli)` digantikan dengan kode pseudonim acak deterministik `CUST_001` hingga `CUST_265`.
  - Informasi wilayah level makro (`kota_kabupaten` dan `provinsi`) dipertahankan untuk kebutuhan analisis pola pengiriman geografis.

### E. Eliminasi Kolom Kosong dan Kolom Konstan (Zero-Variance)
- **Kondisi:** Kolom-kolom berikut tidak memuat variasi data atau bernilai null seluruhnya:
  - `SKU Induk` (100% null).
  - `Diskon Dari Shopee`, `Cashback Koin`, `Paket Diskon (Diskon dari Shopee)`, `Paket Diskon (Diskon dari Penjual)`, `Diskon Kartu Kredit`, `Ongkos Kirim Pengembalian Barang` (semua bernilai 0).
  - `Paket Diskon` (semua bernilai 'N').
  - `Status Pembatalan/ Pengembalian` (hampir seluruhnya null, sisanya hanya 'Permintaan Disetujui').
- **Tindakan:** Seluruh kolom konstan/kosong tersebut dibuang dari dataset pesanan bersih.

### F. Pemisahan Status Selesai dan Batal
- **Kondisi:** Dari 325 pesanan unik, 261 pesanan berstatus `Selesai` dan 64 pesanan berstatus `Batal`.
- **Tindakan:** Kolom `status_pesanan` dipertahankan dalam `data_bersih.csv` sebagai flag pemisah. Disepakati bahwa analisis RFM hanya menyertakan pesanan Selesai, sedangkan pesanan Batal disimpan untuk analisis pola pembatalan di Minggu 5.

---

## 3. Matriks Rekonsiliasi & Kriteria Keberhasilan

| Metrik Validasi | Target Sesuai Readme | Hasil Pembersihan | Status |
|:---|:---:|:---:|:---:|
| Total Pesanan Unik | 325 | 325 | Terpenuhi |
| Pesanan Selesai Unik | 261 | 261 | Terpenuhi |
| Pesanan Batal Unik | 64 | 64 | Terpenuhi |
| Pembeli Selesai Unik (Valid Username) | 229 | 229 | Terpenuhi |
| Pembeli Selesai Unik (Termasuk missing username) | 230 | 230 | Terpenuhi |
| Penggandaan Nilai Uang | Dieliminasi | Dieliminasi (1 baris per pesanan) | Terpenuhi |
| Kolom Privasi PII | 0 Kolom | 0 Kolom | Terpenuhi |
| Eksekusi Ulang Tanpa Error | Kernel restart run-all | Berjalan lancar | Terpenuhi |
