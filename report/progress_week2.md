# Progress Report 2: IN244-Strategi Algoritmik
**Program Studi S-1 Teknik Informatika — Fakultas Teknologi dan Rekayasa Cerdas - Universitas Kristen Maranatha**

---

## I. Identitas Proyek

* **Topik:** (C) Pemilihan Tim Proyek menggunakan metode Branch & Bound
* **Anggota Kelompok:**
    * 2472018 — Kevin Kornelius Martadinata
    * 2472029 — Henry Ferdynand Budiana

---

## II. Ringkasan Topik

Proyek ini bertujuan untuk membangun sistem seleksi kombinasi tim kandidat terbaik berdasarkan kriteria tertentu dari dataset CSV menggunakan algoritma Branch and Bound. Pendekatan ini digunakan untuk memangkas ruang pencarian (search space) secara efisien dibandingkan metode brute force, sehingga pencarian solusi optimal dapat dilakukan dengan waktu eksekusi yang lebih cepat. 

---

## III. Pekerjaan yang Sudah Dikerjakan (Week 2)

* **Persentase Kemajuan Teknis Minggu 2:** 100%
* **Persentase Kemajuan Keseluruhan Proyek:** ~60%
* **Bukti Pengerjaan (GitHub):** [Tubes-Strago/tree/Week2](https://github.com/kevin-krm/Tubes-Strago/tree/Week2)

### Tabel Log Aktivitas dan Fitur Selesai

| No | Kontributor (NRP) | Tugas / Fitur yang Selesai | Status Pengerjaan | Bukti / Link Kode |
| :--- | :--- | :--- | :---: | :--- |
| 1 | 2472018 (Kevin) | Mengimplementasikan fungsi `calculate_bound()` dan logika pemangkasan cabang `prune_branch()`. | Selesai (100%) | [GitHub - branch_bound.py](https://github.com/kevin-krm/Tubes-Strago/commit/2d9082270ee05d604f5dc3b8ded68acf337c8476#diff-e9b09d928a021d894cfae1e396119fb2a00c81553abd6955690499a13b2ca70a) |
| 2 | 2472018 (Kevin) | Mengintegrasikan perhitungan statistik cabang yang dipangkas (*pruning counter*). | Selesai (100%) | [GitHub - branch_bound.py](https://github.com/kevin-krm/Tubes-Strago/commit/2d9082270ee05d604f5dc3b8ded68acf337c8476#diff-e9b09d928a021d894cfae1e396119fb2a00c81553abd6955690499a13b2ca70a) |
| 3 | 2472018 (Kevin) | Melakukan pengujian awal akurasi dan performa menggunakan dataset `medium.csv`. | Selesai Pengujian | - |
| 4 | 2472018 (Kevin) | Membuat planning dan laporan progres minggu kedua. | Selesai | - |
| 5 | 2472029 (Henry) | Mengimplementasikan fungsi inti `branch_and_bound()` pada file `branch_bound.py`. | Selesai (100%) | [GitHub - branch_bound.py](https://github.com/kevin-krm/Tubes-Strago/commit/f66b69e69ab1bc7a203ad7f5e39e61222edf1d7d#diff-e9b09d928a021d894cfae1e396119fb2a00c81553abd6955690499a13b2ca70a) |
| 6 | 2472029 (Henry) | Mengintegrasikan perhitungan statistik total *node* yang dikunjungi. | Selesai (100%) | [GitHub - branch_bound.py](https://github.com/kevin-krm/Tubes-Strago/commit/f66b69e69ab1bc7a203ad7f5e39e61222edf1d7d#diff-e9b09d928a021d894cfae1e396119fb2a00c81553abd6955690499a13b2ca70a) |
| 7 | 2472029 (Henry) | Melakukan pengujian awal akurasi menggunakan dataset `small.csv`. | Selesai Pengujian | - |
| 8 | 2472029 (Henry) | Update dan konversi laporan menjadi github version `progress_week2.md`. | Selesai | - |

---

## IV. Pekerjaan yang Akan Dikerjakan (Week 3)

### Tabel Rencana Tugas dan Skala Prioritas

| No | Daftar Tugas / Fitur | Skala Prioritas | Estimasi Waktu Kerja Aktual |
| :--- | :--- | :---: | :--- |
| 1 | Pembuatan dataset `large.csv`, pengujian performa dataset tersebut, serta optimasi efisiensi kode. | **Tinggi** | 1-3 Jam |
| 2 | Penyusunan dokumen laporan akhir (Semua bab). | **Tinggi** | ~1 Jam |
| 3 | Implementasi fitur tambahan (persentase pruning / ekspor hasil ke TXT). | **Sedang** | 1-2 Jam |
| 4 | Merapikan fungsi `display_result()` di terminal & menyiapkan materi presentasi. | **Sedang** | 1-2 Jam |
| 5 | Improve UI atau membuat program menjadi lebih dinamis/interaktif. | **Rendah** | 1-6 Jam |

*Laporan ini dibuat secara faktual sebagai bentuk pertanggungjawaban progres mingguan pengerjaan Tugas Besar IN244-Strategi Algoritmik 2026.*