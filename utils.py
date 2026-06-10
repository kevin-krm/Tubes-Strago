# file: utils.py
import time
import math
from functools import wraps

## Definisi Fungsi
# execution_timer()
# Decorator untuk menghitung dan mencetak waktu eksekusi sebuah fungsi
def execution_timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        return result, end_time - start_time
    return wrapper

# print_header()
# Mencetak header yang rapi ke konsol
def print_header(title):
    print("\n" + "=" * 55)
    print(f"{title.center(55)}")
    print("=" * 55)

# build_stats_lines()
# Membangun baris-baris statistik lengkap sebagai list string.
# Kamus Lokal:
# n               : jumlah total kandidat (integer)
# k               : ukuran tim yang dicari (integer)
# B               : batas anggaran (float)
# total_cost      : biaya tim terpilih (float)
# nodes_visited   : node yang di-pop dari priority queue (integer)
# nodes_generated : node yang pernah di-push ke priority queue (integer)
# prune_stats     : dict berisi jumlah pruning per alasan (dict)
# exec_time       : waktu eksekusi dalam detik (float)
# lines           : list of string, setiap elemen = satu baris teks
def build_stats_lines(n, k, B, total_cost,
                       nodes_visited, nodes_generated,
                       prune_stats, exec_time):
    lines = []

    # Ruang Kombinasi
    total_combinations = math.comb(n, k)

    # Pruning
    total_pruned  = prune_stats['total']
    pruned_budget = prune_stats['budget']
    pruned_bound  = prune_stats['bound']
    pruned_feasib = prune_stats['feasibility']

    # Persentase pruning: dari seluruh node yang di-generate
    if nodes_generated > 0:
        pruning_pct = (total_pruned / nodes_generated) * 100
    else:
        pruning_pct = 0.0

    # Budget Utilization
    if B > 0 and total_cost > 0:
        budget_util_pct = (total_cost / B) * 100
    else:
        budget_util_pct = 0.0

    lines.append("RUANG PENCARIAN")
    lines.append(f"  Total kandidat (n)         : {n}")
    lines.append(f"  Ukuran tim (k)             : {k}")
    lines.append(f"  Ruang kombinasi C({n},{k})  : {total_combinations:,}")
    lines.append(f"  Node di-generate           : {nodes_generated:,}")
    lines.append(f"  Node dikunjungi (di-pop)   : {nodes_visited:,}")
    lines.append("-" * 55)

    lines.append("PRUNING")
    lines.append(f"  Total cabang dipangkas     : {total_pruned:,}")
    lines.append(f"    - Melebihi anggaran      : {pruned_budget:,}")
    lines.append(f"    - Bound >= best_cost     : {pruned_bound:,}")
    lines.append(f"    - Kandidat tidak cukup   : {pruned_feasib:,}")
    lines.append(f"  Efisiensi pruning          : {pruning_pct:.1f}%  ({total_pruned}/{nodes_generated} node)")
    lines.append("-" * 55)

    lines.append("ANGGARAN")
    lines.append(f"  Batas anggaran (B)         : {B:,.0f}")
    lines.append(f"  Total biaya tim terpilih   : {total_cost:,.0f}")
    lines.append(f"  Budget utilization         : {budget_util_pct:.1f}%  ({total_cost:,.0f} / {B:,.0f})")
    lines.append("-" * 55)

    lines.append("PERFORMA")
    lines.append(f"  Waktu eksekusi             : {exec_time:.5f} detik")

    return lines


# display_result()
# Menampilkan hasil pemilihan tim dan statistik lengkap ke konsol
# Kamus Lokal:
# n : jumlah total kandidat, dihitung dari len(all_candidates) (integer)
def display_result(team, total_cost, k, B, nodes_visited, nodes_generated,
                   prune_stats, nodes_popped_and_pruned, exec_time,
                   all_candidates=None):

    n = len(all_candidates) if all_candidates else 0
    print_header("HASIL PEMILIHAN TIM PROYEK")

    if not team:
        print("Tidak ada kombinasi tim yang memenuhi kriteria.")
    else:
        print(f"Target Anggota Tim (k) : {k} orang")
        print(f"Batas Anggaran (B)     : {B}\n")

        print("Daftar Anggota Tim Terpilih:")
        for i, member in enumerate(team, start=1):
            print(f"  {i}. {member.nama} (ID: {member.id}, Cost: {member.cost})")

        print("-" * 55)
        print(f"Total Biaya Tim        : {total_cost}")

    print_header("STATISTIK BRANCH & BOUND")
    for line in build_stats_lines(n, k, B, total_cost,
                                   nodes_visited, nodes_generated,
                                   prune_stats, exec_time):
        print(line)
    print("=" * 55 + "\n")


# export_to_txt()
# Mengekspor hasil pemilihan tim dan statistik ke berkas TXT
# Kamus Lokal:
# target_path : path file output di dalam folder 'exports' (string)
def export_to_txt(file_path, team, total_cost, k, B,
                  nodes_visited, nodes_generated,
                  prune_stats, nodes_popped_and_pruned, exec_time,
                  all_candidates=None):
    import os

    n = len(all_candidates) if all_candidates else 0
    target_path = os.path.join("exports", os.path.basename(file_path))

    try:
        with open(target_path, mode='w', encoding='utf-8') as f:
            f.write("=" * 55 + "\n")
            f.write(f"{'HASIL PEMILIHAN TIM PROYEK'.center(55)}\n")
            f.write("=" * 55 + "\n")

            if not team:
                f.write("Tidak ada kombinasi tim yang memenuhi kriteria.\n")
            else:
                f.write(f"Target Anggota Tim (k) : {k} orang\n")
                f.write(f"Batas Anggaran (B)     : {B}\n\n")

                f.write("Daftar Anggota Tim Terpilih:\n")
                for i, member in enumerate(team, start=1):
                    f.write(f"  {i}. {member.nama} (ID: {member.id}, Cost: {member.cost})\n")

                f.write("-" * 55 + "\n")
                f.write(f"Total Biaya Tim        : {total_cost}\n")

            f.write("\n" + "=" * 55 + "\n")
            f.write(f"{'STATISTIK BRANCH & BOUND'.center(55)}\n")
            f.write("=" * 55 + "\n")
            for line in build_stats_lines(n, k, B, total_cost,
                                           nodes_visited, nodes_generated,
                                           prune_stats, exec_time):
                f.write(line + "\n")
            f.write("=" * 55 + "\n")

        return True, target_path
    except Exception as e:
        print(f"[Error] Gagal mengekspor hasil ke berkas TXT: {e}")
        return False, ""