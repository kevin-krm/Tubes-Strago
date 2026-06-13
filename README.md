# Tubes-Strago — Pemilihan Tim Proyek (Branch & Bound)

Tugas Besar **IN244 — Strategi Algoritmik**, S-1 Teknik Informatika, Universitas Kristen Maranatha.

Kontributor:
- 2472018 - Kevin Kornelius Martadinata
- 2472029 - Henry Ferdynand Budiana

---

Aplikasi memilih **k** kandidat dari **n** kandidat agar **total biaya minimum** dan tidak melebihi batas anggaran **B**, menggunakan algoritma **Branch & Bound** (least-cost search + pruning) untuk menjamin solusi optimal. Tersedia dua antarmuka: **CLI terminal** dan **web visualisasi** yang menampilkan jalannya pohon pencarian langkah demi langkah.

* **Anggota:** 2472018 — Kevin Kornelius Martadinata · 2472029 — Henry Ferdynand Budiana

## Teknologi

| Kategori | Yang dipakai |
| :--- | :--- |
| Bahasa Pemrograman Algoritma | Python 3 |
| Framework web | Flask (untuk `app.py`) |
| Frontend | HTML + CSS + JavaScript (vanilla, tanpa build tool) · SVG untuk pohon pencarian |
| Pustaka standar | `heapq` (priority queue), `csv`, `math`, `time` |
| Data | CSV (`datasets/small.csv` n=12, `medium.csv` n=18, `large.csv` n=24) |

> Inti algoritma (`branch_bound.py`, `csv_loader.py`, `candidate.py`, `utils.py`) hanya memakai pustaka standar Python.

> **Dependensi eksternal tidak diperlukan**. 
> Flask hanya diperlukan untuk visualisasi via antarmuka web.

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

### Antarmuka web (visualisasi)
```bash
python app.py
```
Lalu buka **http://localhost:5000** di browser.

### Antarmuka CLI (terminal)
```bash
python main.py
```

## Setup saat clone ke device lain

Sebelum menjalankan `python app.py` di komputer lain, lakukan langkah berikut:

1. **Pastikan Python 3 terpasang** (cek: `python --version`).
2. **(Opsional, disarankan) buat virtual environment:**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```
3. **Pasang dependensi** (hanya Flask):
   ```bash
   pip install -r requirements.txt

   # Bila tidak bekerja
   python -m pip install "flask>=3.0"

   ```
4. **Jalankan:**
   ```bash
   python app.py
   ```

> Catatan:
> - `main.py` (CLI) bisa langsung dijalankan tanpa langkah 3 karena tidak memakai Flask.
> - Jika **port 5000** sudah dipakai aplikasi lain, set port lain via environment variable, mis. (Windows PowerShell) `$env:PORT=8000; python app.py`.
> - Jalankan perintah dari **folder root proyek** agar path relatif ke `datasets/` dan `templates/` terbaca dengan benar.
