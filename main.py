# file: main.py
import sys
from utils import print_header, display_result, execution_timer, export_to_txt
from candidate import Candidate
from csv_loader import load_csv, display_candidates
from branch_bound import branch_and_bound

def main():
    print_header("APLIKASI PEMILIHAN TIM PROYEK (BRANCH & BOUND)")
    while True:
        # Loop untuk input k (akan terus berulang langsung jika tidak valid)
        while True:
            try:
                k_input = input("Masukkan jumlah anggota tim yang dibutuhkan (k): ")
                k = int(k_input)
            except ValueError:
                print("Input tidak valid! Harap masukkan angka.\n")
                continue

            if not (5 <= k <= 10):
                print("> [Notice] Input tidak valid, input range (5 <= k <= 10)\n")
                continue

            break

        # Input batas anggaran (B) - jika gagal, ulangi dari input k
        try:
            B_input = input("Masukkan batas anggaran maksimal (B): ")
            B = int(B_input)
        except ValueError:
            print("Input tidak valid! Harap masukkan angka.\n")
            continue

        # Input dataset - jika gagal, ulangi dari input k
        dataset_choice = input("Pilih dataset (1: Small, 2: Medium, 3: Large): ")

        file_path = ""
        dataset_name = ""
        if dataset_choice == '1':
            file_path = "datasets/small.csv"
            dataset_name = "Small"
        elif dataset_choice == '2':
            file_path = "datasets/medium.csv"
            dataset_name = "Medium"
        elif dataset_choice == '3':
            file_path = "datasets/large.csv"
            dataset_name = "Large"
        else:
            print("> [Notice] Pilihan dataset tidak dikenali.\n")
            continue

        print(f"\n[INFO] Membaca data dari {file_path}...")
        candidates = load_csv(file_path)

        if not candidates:
            print("[Error] Tidak ada data kandidat yang berhasil dimuat.\n")
            continue

        display_candidates(candidates)

        # Validasi budget: cek apakah B cukup untuk memilih k orang - jika tidak, ulangi dari input k
        min_budget = sum(sorted(c.cost for c in candidates)[:k])
        if B < min_budget:
            print(f"[Error] Budget B = {B} tidak mencukupi untuk memilih {k} orang.")
            print(f"        Minimum budget yang dibutuhkan : {min_budget}")
            print(f"        (Dihitung dari {k} kandidat dengan biaya terendah)\n")
            continue

        # Seluruh input valid, keluar dari loop utama
        break

    print(f"[INFO] Menjalankan Algoritma Branch & Bound untuk k={k}, B={B}...")

    @execution_timer
    def run_algorithm():
        return branch_and_bound(candidates, k, B)

    (team, total_cost, nodes_visited, nodes_generated, prune_stats, nodes_popped_and_pruned), exec_time = run_algorithm()

    display_result(
        team, total_cost, k, B, nodes_visited, nodes_generated, prune_stats, nodes_popped_and_pruned, exec_time, all_candidates=candidates, dataset_name=dataset_name
    )

    # Menanyakan apakah pengguna ingin mengekspor hasil pencarian ke file TXT
    export_choice = input("Apakah Anda ingin mengekspor hasil ke berkas TXT? (y/n): ").strip().lower()
    if export_choice == 'y':
        file_name = input("Masukkan nama berkas (kosongkan untuk default 'hasil_pemilihan.txt'): ").strip()
        if not file_name:
            file_name = "hasil_pemilihan.txt"
        elif not file_name.endswith(".txt"):
            file_name += ".txt"

        success, final_path = export_to_txt(
            file_name, team, total_cost, k, B, nodes_visited, nodes_generated, prune_stats, nodes_popped_and_pruned, exec_time, all_candidates=candidates, dataset_name=dataset_name
        )
        if success:
            print(f"\n[INFO] Berhasil mengekspor hasil ke berkas '{final_path}'!")
        else:
            print("\n[Error] Gagal mengekspor hasil.")

if __name__ == "__main__":
    main()