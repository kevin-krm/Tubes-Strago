# file: main.py
import sys
from utils import print_header, display_result, execution_timer, export_to_txt, build_stats_lines
from candidate import Candidate
from csv_loader import load_csv, display_candidates
from branch_bound import branch_and_bound
from sensitivity import run_sensitivity, build_sensitivity_lines, K_MIN, K_MAX
from pdf_export import build_pdf

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

    # Menu lanjutan: ekspor (TXT/PDF) dan analisis sensitivitas
    post_result_menu(team, total_cost, k, B, candidates, dataset_name,
                     nodes_visited, nodes_generated, prune_stats,
                     nodes_popped_and_pruned, exec_time)


# post_result_menu()
# Menampilkan opsi pasca-hasil: ekspor TXT, ekspor PDF, dan analisis sensitivitas.
# Hasil sensitivitas terakhir disimpan agar dapat disertakan ke berkas PDF.
# Kamus Lokal:
# last_sensitivity : dict {vary, fixed_label, rows} hasil analisis terakhir (atau None)
# choice           : pilihan menu pengguna (string)
def post_result_menu(team, total_cost, k, B, candidates, dataset_name,
                     nodes_visited, nodes_generated, prune_stats,
                     nodes_popped_and_pruned, exec_time):
    last_sensitivity = None

    while True:
        print("\n" + "-" * 55)
        print("OPSI LANJUTAN")
        print("  1. Ekspor hasil ke berkas TXT")
        print("  2. Ekspor hasil ke berkas PDF")
        print("  3. Analisis sensitivitas (variasikan B atau k)")
        print("  4. Selesai")
        choice = input("Pilih opsi (1-4): ").strip()

        if choice == '1':
            file_name = input("Nama berkas (kosongkan untuk 'hasil_pemilihan.txt'): ").strip()
            if not file_name:
                file_name = "hasil_pemilihan.txt"
            elif not file_name.endswith(".txt"):
                file_name += ".txt"
            success, final_path = export_to_txt(
                file_name, team, total_cost, k, B, nodes_visited, nodes_generated,
                prune_stats, nodes_popped_and_pruned, exec_time,
                all_candidates=candidates, dataset_name=dataset_name)
            if success:
                print(f"\n[INFO] Berhasil mengekspor hasil ke berkas '{final_path}'!")
            else:
                print("\n[Error] Gagal mengekspor hasil.")

        elif choice == '2':
            stats_lines = build_stats_lines(
                len(candidates), k, B, total_cost, nodes_visited, nodes_generated,
                prune_stats, exec_time, nodes_popped_and_pruned)
            file_name = input("Nama berkas (kosongkan untuk 'hasil_pemilihan.pdf'): ").strip()
            if not file_name:
                file_name = "hasil_pemilihan.pdf"
            try:
                final_path = build_pdf(
                    file_name, team=team, total_cost=total_cost, k=k, B=B,
                    dataset_name=dataset_name, stats_lines=stats_lines,
                    sensitivity=last_sensitivity)
                note = " (termasuk analisis sensitivitas)" if last_sensitivity else ""
                print(f"\n[INFO] Berhasil mengekspor PDF ke berkas '{final_path}'!{note}")
            except Exception as e:
                print(f"\n[Error] Gagal mengekspor PDF: {e}")

        elif choice == '3':
            last_sensitivity = run_sensitivity_cli(candidates, k, B) or last_sensitivity

        elif choice == '4':
            break

        else:
            print("> [Notice] Pilihan tidak dikenali.")


# run_sensitivity_cli()
# Memandu input rentang analisis sensitivitas, menjalankannya, mencetak tabel teks,
# dan mengembalikan dict {vary, fixed_label, rows} (atau None bila dibatalkan).
def run_sensitivity_cli(candidates, k, B):
    vary = input("Variasikan parameter mana? (B/k): ").strip().lower()
    if vary == 'b':
        vary = 'B'
    if vary not in ('B', 'k'):
        print("> [Notice] Pilihan parameter tidak dikenali.")
        return None

    try:
        if vary == 'B':
            lo = int(input("  Anggaran minimum: "))
            hi = int(input("  Anggaran maksimum: "))
            step = int(input("  Langkah (step): "))
        else:
            lo = int(input(f"  k minimum ({K_MIN}-{K_MAX}): "))
            hi = int(input(f"  k maksimum ({K_MIN}-{K_MAX}): "))
            step = 1
    except ValueError:
        print("> [Notice] Input rentang tidak valid (harus angka).")
        return None

    if step <= 0 or lo > hi:
        print("> [Notice] Rentang tidak valid (pastikan step > 0 dan min <= max).")
        return None

    rows = run_sensitivity(candidates, k, B, vary, lo, hi, step)
    if not rows:
        print("> [Notice] Tidak ada titik analisis dalam rentang tersebut.")
        return None

    fixed_label = f"k = {k}" if vary == 'B' else f"B = {B:,.0f}"
    print()
    for line in build_sensitivity_lines(rows, vary, fixed_label):
        print(line)

    return {"vary": vary, "fixed_label": fixed_label, "rows": rows}


if __name__ == "__main__":
    main()