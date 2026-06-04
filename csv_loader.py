import csv
import os
from candidate import Candidate

# Membaca data kandidat dari file CSV dan mengembalikan list objek Candidate
def load_csv(file_path: str) -> list:
    candidates = []
    
    # Validasi apakah file ada
    if not os.path.exists(file_path):
        print(f"[Error] File tidak ditemukan di path: {file_path}")
        return candidates

    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            # Validasi header CSV
            required_headers = {'id', 'nama', 'cost'}
            if not required_headers.issubset(reader.fieldnames):
                print("[Error] Format CSV salah. Pastikan memiliki kolom: id, nama, cost.")
                return candidates

            for row in reader:
                try:
                    # Mengonversi tipe data cost ke float/int untuk kalkulasi algoritma
                    kandidat_obj = Candidate(
                        id_kandidat=row['id'].strip(),
                        nama=row['nama'].strip(),
                        cost=float(row['cost'].strip())
                    )
                    candidates.append(kandidat_obj)
                except ValueError:
                    print(f"[Warning] Melewati baris data cacat (nilai cost tidak valid): {row}")
                    
    except Exception as e:
        print(f"[Error] Terjadi kesalahan saat membaca file: {e}")
    return candidates

# Menampilkan seluruh daftar kandidat yang tersedia ke terminal.
def display_candidates(candidates: list):
    if not candidates:
        print("Tidak ada data kandidat untuk ditampilkan.")
        return

    print(f"\n{'='*40}")
    print(f"{'DAFTAR KANDIDAT YANG TERSEDIA':^40}")
    print(f"{'='*40}")
    print(f"{'ID':<6} | {'Nama Kandidat':<20} | {'Cost':<10}")
    print(f"{'-'*40}")
    for c in candidates:
        print(f"{c.id:<6} | {c.nama:<20} | {c.cost:<10.2f}")
    print(f"{'='*40}\n")