# file: branch_bound.py
# Implementasi algoritma Branch and Bound untuk pemilihan tim proyek

import heapq

# calculate_bound()
# Menghitung estimasi lower bound dari suatu node dalam pohon pencarian Branch and Bound

# Kamus Lokal:
# candidates   : daftar kandidat yang sudah diurutkan berdasarkan cost (list)
# start_index  : indeks kandidat pertama yang masih tersedia (integer)
# selected     : daftar kandidat yang sudah dipilih (list)
# k            : jumlah anggota tim yang harus dipenuhi (integer)
# current_cost : total biaya sementara (float)
# slots_needed : jumlah slot anggota tim yang masih dibutuhkan (integer)
# remaining    : daftar kandidat yang masih tersedia (list)
# bound        : nilai lower bound biaya minimum (float)
# i            : counter (integer)
def calculate_bound(candidates: list, start_index: int, selected: list,k: int, current_cost: float) -> float:
    slots_needed = k - len(selected)
    # Jika tidak ada slot lagi yang dibutuhkan, bound = current_cost
    if slots_needed == 0:
        return current_cost
    # Kumpulkan kandidat yang tersisa mulai dari start_index
    remaining = candidates[start_index:]
    # Jika kandidat tersisa kurang dari slot yang masih dibutuhkan, state ini tidak mungkin menghasilkan solusi valid (bound = inf)
    if len(remaining) < slots_needed:
        return float('inf')
    # Tambahkan cost dari 'slots_needed' kandidat termurah yang tersisa (list sudah terurut, jadi ambil elemen pertama)
    bound = current_cost
    for i in range(slots_needed):
        bound += remaining[i].cost

    return bound

# prune_branch()
# Menentukan apakah sebuah node/cabang harus dipangkas (pruning)

# Kamus Lokal:
# bound        : nilai lower bound node saat ini (float)
# current_cost : total biaya node saat ini (float)
# B            : batas anggaran maksimum (float)
# best_cost    : biaya terbaik yang sudah ditemukan (float)
# slots_needed : jumlah slot anggota yang masih dibutuhkan (integer)
# remaining    : jumlah kandidat yang masih tersedia (integer)
def prune_branch(bound: float, current_cost: float, B: float,best_cost: float, slots_needed: int, remaining: int) -> tuple:
    # Jika biaya sudah melebihi anggaran, pangkas cabang
    if current_cost > B:
        return True, "budget"
    # Jika solusi terbaik yang mungkin dicapai tidak lebih baik dari solusi saat ini, pangkas cabang
    if bound >= best_cost:
        return True, "bound"
    # Jika kandidat tersisa tidak cukup untuk memenuhi kuota tim, pangkas cabang
    if remaining < slots_needed:
        return True, "feasibility"
    # Cabang masih layak untuk dieksplorasi
    return False, ''

# branch_and_bound()
# Fungsi utama algoritma Branch and Bound untuk memilih tepat k kandidat dengan total biaya minimum yang tidak melebihi anggaran B.