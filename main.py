# file: main.py
import sys
from utils import print_header, display_result, execution_timer
from candidate import Candidate
from csv_loader import load_csv, display_candidates
from branch_bound import branch_and_bound

def main():
    print_header("APLIKASI PEMILIHAN TIM PROYEK (BRANCH & BOUND)")
    try:
        k = int(input("Masukkan jumlah anggota tim yang dibutuhkan (k): "))
        B = float(input("Masukkan batas anggaran maksimal (B): "))
        dataset_choice = input("Pilih dataset (1: Small, 2: Medium, 3: Large): ")
    except ValueError:
        print("\nInput tidak valid! Harap masukkan angka.")
        sys.exit(1)

    # Validasi nilai k (5 <= k <= 10)
    if not (5 <= k <= 10):
        print("\n[Error] Nilai k harus berada di antara 5 dan 10.")
        sys.exit(1)

    file_path = ""
    if dataset_choice == '1':
        file_path = "datasets/small.csv"
    elif dataset_choice == '2':
        file_path = "datasets/medium.csv"
    elif dataset_choice == '3':
        file_path = "datasets/large.csv"
    else:
        print("\nPilihan dataset tidak dikenali.")
        sys.exit(1)

    print(f"\n[INFO] Membaca data dari {file_path}...")
    candidates = load_csv(file_path)

    if not candidates:
        print("[Error] Tidak ada data kandidat yang berhasil dimuat.")
        sys.exit(1)

    display_candidates(candidates)
    print(f"[INFO] Menjalankan Algoritma Branch & Bound untuk k={k}, B={B}...")

    @execution_timer
    def run_algorithm():
        return branch_and_bound(candidates, k, B)

    (team, total_cost, nodes, pruned), exec_time = run_algorithm()

    display_result(team, total_cost, k, B, nodes, pruned, exec_time)

if __name__ == "__main__":
    main()