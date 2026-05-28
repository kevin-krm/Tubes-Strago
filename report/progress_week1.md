# Progress Report 1: IN244-Strategi Algoritmik
**Program Studi S-1 Teknik Informatika — Fakultas Teknologi dan Rekayasa Cerdas - ** **Universitas Kristen Maranatha**

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

## III. Pekerjaan yang Sudah Dikerjakan (Week 1)

Fokus pada minggu ini adalah membangun fondasi utama proyek, menyiapkan struktur berkas kode, merancang arsitektur pencarian algoritma, serta menyelesaikan modul pembacaan data (I/O). 

* **Persentase Kemajuan Minggu 1:** 100%
* **Persentase Kemajuan Keseluruhan Proyek:** 33.5%

### Tabel Log Aktivitas dan Fitur Selesai

| No | Kontributor (NRP - Nama) | Tugas / Fitur yang Selesai | Bukti / Link Kode |
| :--- | :--- | :--- | :--- |
| 1 | 2472018 (Kevin) | Membuat model data kelas `Candidate` di berkas `candidate.py` untuk representasi objek kandidat. | [GitHub - candidate.py](https://github.com/kevin-krm/Tubes-Strago/blob/Week1/candidate.py) |
| 2 | 2472018 (Kevin) | Membangun modul parser data `csv_loader.py` yang berisi implementasi fungsi `load_csv()` untuk membaca dataset. | [GitHub - csv_loader.py](https://github.com/kevin-krm/Tubes-Strago/blob/Week1/csv_loader.py) |
| 3 | 2472018 (Kevin) | Menyiapkan berkas pengujian awal `small.csv` di dalam folder dataset dan menyediakan fungsi penampil `display_candidates()`. | [GitHub - datasets/](https://github.com/kevin-krm/Tubes-Strago/tree/Week1/datasets) |
| 4 | 2472029 (Henry) | Melakukan analisis teoretis algoritma, merancang visualisasi alur logika (*flowchart*), serta menyusun *pseudocode* Branch and Bound. | [GitHub - laporan/](https://github.com/kevin-krm/Tubes-Strago/blob/Week1/report) |
| 5 | 2472029 (Henry) | Menginisialisasi pohon direktori repositori serta membangun kerangka interaksi terminal utama pada file `main.py`. | [GitHub - main.py](https://github.com/kevin-krm/Tubes-Strago/blob/Week1/main.py) |
| 6 | 2472029 (Henry) | Membuat modul pembantu `utils.py` yang mengimplementasikan fungsi dekorator `@execution_timer` dan perapian struktur teks *output*. | [GitHub - utils.py](https://github.com/kevin-krm/Tubes-Strago/blob/Week1/utils.py) |

---

## IV. Pekerjaan yang Akan Dikerjakan (Week 2)

Rencana kerja untuk minggu berikutnya akan berfokus pada implementasi mesin pencarian algoritma utama, logika kalkulasi batas bawah (*lower bound*), fungsi pemangkasan (*pruning*), serta integrasi pengujian fungsionalitas program.

### Tabel Rencana Tugas dan Skala Prioritas

| No | Daftar Tugas / Fitur | Skala Prioritas | Estimasi Waktu Kerja |
| :--- | :--- | :---: | :--- |
| 1 | Implementasi fungsi inti pembentuk pohon status `branch_and_bound()` dan fungsi estimasi batas bawah `calculate_bound()` di dalam berkas `branch_bound.py`. | **Tinggi** | ~2 hari |
| 2 | Pengembangan logika pengecekan kondisi batas anggaran dan jumlah kuota tim untuk memicu pemangkasan cabang (*prune_branch*) secara real-time. | **Tinggi** | ~2 hari |
| 3 | Integrasi variabel pencatat performa statistik B&B, mencakup penghitung total *node* yang dikunjungi dan jumlah simpul hidup yang berhasil dipangkas. | **Sedang** | <1 hari |
| 4 | Pengujian akurasi fungsionalitas algoritma serta komparasi kecepatan eksekusi data menggunakan variasi berkas `small.csv` dan `medium.csv`. | **Sedang** | ~1 hari |

---
*Laporan ini dibuat secara faktual sebagai bentuk pertanggungjawaban progres mingguan pengerjaan Tugas Besar IN244-Strategi Algoritmik 2026.*