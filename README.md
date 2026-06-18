# Tubes-Strago — Pemilihan Tim Proyek (Branch & Bound)

Tugas Besar **IN244 — Strategi Algoritmik**, S-1 Teknik Informatika, Universitas Kristen Maranatha.

Kontributor:
- 2472018 - Kevin Kornelius Martadinata
- 2472029 - Henry Ferdynand Budiana

---

Aplikasi memilih **k** kandidat dari **n** kandidat agar **total biaya minimum** dan tidak melebihi batas anggaran **B**, menggunakan algoritma **Branch & Bound** (least-cost search + pruning) untuk menjamin solusi optimal. Tersedia dua antarmuka: **CLI terminal** dan **web visualisasi** yang menampilkan jalannya pohon pencarian langkah demi langkah.

## Teknologi

| Kategori | Yang dipakai |
| :--- | :--- |
| Bahasa Pemrograman Algoritma | Python 3 |
| Framework web | Flask (untuk `app.py`) |
| Frontend | HTML + CSS + JavaScript (vanilla) + SVG untuk pohon pencarian |
| Pustaka standar | `heapq` (priority queue), `csv`, `math`, `time` |
| Data | CSV (`datasets/small.csv` n=12, `medium.csv` n=18, `large.csv` n=24) |

> Inti algoritma (`branch_bound.py`, `csv_loader.py`, `candidate.py`, `utils.py`) hanya memakai pustaka standar Python.

> **Dependensi eksternal tidak diperlukan**. 
> Flask dan Reportlab hanya diperlukan untuk visualisasi via antarmuka web.

## Struktur singkat

```
branch_bound.py   # inti algoritma Branch & Bound
candidate.py      # model data kandidat
csv_loader.py     # pembacaan dataset CSV
utils.py          # statistik, tampilan, ekspor TXT
main.py           # antarmuka CLI terminal
app.py            # server web (Flask)
templates/        # halaman visualisasi (index.html)
datasets/         # small / medium / large
```

## Cara menjalankan

### Antarmuka web (visualisasi) lihat setup dibawah
```bash
python app.py
```
Lalu buka **http://localhost:5000** di browser.

### Antarmuka CLI (terminal)
```bash
python main.py
```

## Setup

Bila belum ada dependency untuk aplikasi ini, lakukan langkah berikut:

1. **Pastikan Python 3 terpasang** (cek: `python --version`).
2. **(Opsional, disarankan) buat virtual environment:**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```
3. **Pasang dependensi**:
   ```bash
   # install semua dependensi
   pip install -r requirements.txt

   # bila tidak bekerja
   py -m pip install -r requirements.txt

   # atau install satuan
   py -m pip install reportlab
   py -m pip install "flask>=3.0"
   ```

4. **Jalankan web server:**
   ```bash
   python app.py
   ```

> Catatan:
> - Jika **port 5000** sudah dipakai aplikasi lain, set port lain via environment variable, mis. (Windows PowerShell) `$env:PORT=8000; python app.py`.
> - Jalankan perintah dari **folder root proyek** agar path relatif ke `datasets/` dan `templates/` terbaca dengan benar.
