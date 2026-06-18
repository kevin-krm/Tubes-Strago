# Progress Report 3: IN244-Strategi Algoritmik
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

## III. Pekerjaan yang Sudah Dikerjakan (Week 3)

Fokus pada minggu ini adalah penyelesaian seluruh fitur program, pengujian performa pada tiga skala dataset, perbaikan konsistensi pelaporan statistik B&B, serta peningkatan interaktivitas antarmuka terminal.

* **Persentase Kemajuan Teknis Minggu 3:** 100%
* **Persentase Kemajuan Keseluruhan Proyek:** ~90%

**Bukti Pengerjaan (GitHub):**

### Tabel Log Aktivitas dan Fitur Selesai

| No | Kontributor (NRP) | Tugas / Fitur yang Selesai | Status Pengerjaan | Bukti / Link Kode |
| :--- | :--- | :--- | :---: | :--- |
| 1 | 2472018 (Kevin) | Melakukan pengujian performa program menggunakan dataset large. | Selesai (100%) | [GitHub - large.csv](https://github.com/kevin-krm/Tubes-Strago/commit/52c6b4915dfc65d152a37ea3a1fbdcd4f9f21005#diff-93a730bd7d210e30c3c102a8c08d84dbaac61cb466bfbed67ce285e12f01b855) |
| 2 | 2472018 (Kevin) | Menerapkan fitur tambahan unik (seperti mencetak persentase pruning atau ekspor hasil ke berkas TXT). | Selesai (100%) | [GitHub - 50e9385](https://github.com/kevin-krm/Tubes-Strago/commit/50e9385b28f27de79cfb2774a26514ff109c60e3) |
| 3 | 2472018 (Kevin) | Menambahkan validasi anggaran minimum: program menampilkan pesan informatif jika nilai B tidak mencukupi untuk memilih k kandidat. | Selesai (100%) | [GitHub - 2771a64](https://github.com/kevin-krm/Tubes-Strago/commit/2771a6482628b9086beb592501755290b4872e64) |
| 4 | 2472018 (Kevin) | Membuat planning dan laporan progres minggu kedua | Selesai | - |
| 5 | 2472018 (Kevin) | Menyusun dokumen laporan akhir proyek bab analisis dan implementasi kode | 50% | - |
| 6 | 2472029 (Henry) | Melakukan optimasi kode program agar waktu eksekusi lebih efisien | Selesai (100%) | [GitHub - b419d63](https://github.com/kevin-krm/Tubes-Strago/commit/b419d63719cf58ed13442c22345c2a835d870765) |
| 7 | 2472029 (Henry) | Refaktor fungsi `branch_and_bound()` dengan mengekstrak helper `consider_child()` untuk menyatukan logika pruning kedua cabang (ambil/tidak ambil) yang sebelumnya terduplikasi. | Selesai (100%) | [GitHub - b419d63](https://github.com/kevin-krm/Tubes-Strago/commit/b419d63719cf58ed13442c22345c2a835d870765) |
| 8 | 2472029 (Henry) | Merapikan fungsi display_result() untuk tampilan output terminal akhir agar informatif dan bersih. | Selesai (100%) | [GitHub - main.py](https://github.com/kevin-krm/Tubes-Strago/commit/b419d63719cf58ed13442c22345c2a835d870765#diff-b10564ab7d2c520cdd0243874879fb0a782862c3c902ab535faabe57d5a505e1) |
| 9 | 2472029 (Henry) | Update dan konversi laporan progres minggu ketiga menjadi `.md`. | Selesai | - |
| 10 | 2472029 (Henry) | Menyusun dokumen laporan akhir bagian hasil pengujian statistik, serta menyiapkan materi presentasi. | 20% | - |

---

## IV. Pekerjaan yang Akan Dikerjakan (Week 4 / Final)

### Tabel Rencana Tugas dan Skala Prioritas

| No | Daftar Tugas / Fitur | Skala Prioritas | Estimasi Waktu Kerja Aktual |
| :--- | :--- | :---: | :--- |
| 1 | Penyusunan dokumen laporan akhir (semua bab: pendahuluan, analisis, implementasi, pengujian, kesimpulan). | **Tinggi** | 3-5 Jam |
| 2 | Penyusunan dan latihan materi presentasi akhir. | **Tinggi** | 2-3 Jam |
| 3 | Pengujian akhir menyeluruh (edge case: B ketat, k maksimum, dataset large). | **Sedang** | 1-2 Jam |
| 4 | Pembersihan kode (*cleanup*, komentar, kerapian repositori). | **Rendah** | <1 Jam |
| 5 | Improve UI atau membuat program menjadi lebih dinamis/interaktif. | **Rendah** | 3-6 Jam |

*Laporan ini dibuat secara faktual sebagai bentuk pertanggungjawaban progres mingguan pengerjaan Tugas Besar IN244-Strategi Algoritmik 2026.*