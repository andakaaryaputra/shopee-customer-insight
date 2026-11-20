# Kamus Data: Tabel Pesanan Bersih (`data_bersih.csv`)

Dokumen ini memuat definisi, tipe data, aturan pembersihan, dan contoh nilai untuk setiap kolom pada tabel pesanan bersih hasil pembersihan data transaksi Shopee Seller (Minggu 1).

---

## 1. Ringkasan Struktur Tabel
- **Nama File:** `data_bersih.csv`
- **Tingkat Agregasi:** Tingkat Pesanan (*Order-Level*). Satu baris merepresentasikan 1 pesanan unik (`id_pesanan`).
- **Dimensi:** 325 baris, 13 kolom.
- **Komposisi Status:**
  - `Selesai`: 261 pesanan.
  - `Batal`: 64 pesanan.
- **Rentang Transaksi:** 10 Juli 2024 s.d. 27 November 2025.

---

## 2. Rincian Kolom

| No | Nama Kolom | Tipe Data | Deskripsi & Aturan Pembersihan | Contoh Nilai |
|:---|:---|:---|:---|:---|
| 1 | `id_pesanan` | String / Text | Nomor identifikasi transaksi unik Shopee (asli: `No. Pesanan`). Berfungsi sebagai primary key. | `24071068800VVR` |
| 2 | `id_pembeli` | String / Text | ID pembeli hasil anonimisasi (menggantikan `Username (Pembeli)` asli untuk kepatuhan privasi data). Format: `CUST_001` - `CUST_265`. Satu nilai missing diisi identifier khusus sebelum pemetaan. | `CUST_042` |
| 3 | `status_pesanan` | String / Category | Status akhir pesanan di Shopee (`Selesai` atau `Batal`). Status `Selesai` digunakan untuk analisis RFM (Minggu 2), sedangkan `Batal` dianalisis terpisah (Minggu 5). | `Selesai`, `Batal` |
| 4 | `waktu_pesanan_dibuat` | Datetime (`YYYY-MM-DD HH:MM:SS`) | Waktu saat pembeli membuat pesanan di sistem Shopee. Digunakan sebagai dasar penghitungan *Recency*. | `2024-07-10 14:22:00` |
| 5 | `waktu_pembayaran_dilakukan` | Datetime (`YYYY-MM-DD HH:MM:SS`) | Waktu saat pembayaran berhasil diverifikasi oleh Shopee. Nilai `-` (pesanan belum dibayar) diubah menjadi null/NaT. | `2024-07-10 14:25:00` |
| 6 | `waktu_pesanan_selesai` | Datetime (`YYYY-MM-DD HH:MM:SS`) | Waktu saat pesanan dikonfirmasi selesai oleh pembeli atau sistem. Bernilai null/NaT untuk pesanan berstatus Batal. | `2024-07-13 18:30:00` |
| 7 | `metode_pembayaran` | String / Category | Metode pembayaran yang dipilih pembeli (e.g., COD, Saldo ShopeePay, SPayLater, Transfer Bank). | `COD (Bayar di Tempat)` |
| 8 | `opsi_pengiriman` | String / Text | Jenis kurir dan layanan logistik pengiriman (e.g., Reguler Anteraja, SPX Standard, Hemat). | `Reguler (Cashless)-Anteraja` |
| 9 | `total_pembayaran_rp` | Float64 / Numeric | Total nilai uang yang dibayarkan pembeli dalam Rupiah (IDR). Tanda titik ribuan telah dikonversi ke angka riil. Diambil 1 kali per pesanan (tidak terduplikasi per item). | `134000.0` |
| 10 | `kota_kabupaten` | String / Text | Kota atau kabupaten tujuan pengiriman (data geografis agregat non-privasi). | `KOTA JAKARTA SELATAN` |
| 11 | `provinsi` | String / Text | Wilayah administratif provinsi alamat pengiriman pembeli. | `DKI JAKARTA` |
| 12 | `alasan_pembatalan` | String / Text | Alasan pembatalan pesanan dari sistem Shopee atau pembeli. Bernilai null/NaN jika pesanan berstatus Selesai. | `Pesanan belum dibayar` |
| 13 | `jumlah_pengembalian` | Integer / Numeric | Total kuantitas barang yang dikembalikan/retur pada pesanan tersebut (diambil dari agregasi `Returned quantity`). | `0`, `1` |

---

## 3. Catatan Penggunaan untuk Minggu Berikutnya
1. **Analisis RFM (Minggu 2 - 4):** Filter tabel hanya pada baris `status_pesanan == 'Selesai'`. Total baris yang digunakan adalah 261 pesanan dengan 229 pembeli unik (atau 230 jika menyertakan pembeli tanpa username asli).
2. **Analisis Pola Transaksi & Pembatalan (Minggu 5):** Gunakan seluruh tabel pesanan untuk menganalisis tren metode pembayaran, waktu transaksi, sebaran provinsi, serta 64 pesanan yang dibatalkan.
