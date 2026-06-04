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
def branch_and_bound(candidates: list, k: int, B: float):
    # Mengurutkan kandidat berdasarkan cost dari yang termurah (Least Cost Search)
    candidates.sort(key=lambda x: x.cost)
    
    Q = [] # Priority Queue
    best_solution = []
    min_cost = float('inf')
    nodes_visited = 0
    branches_pruned = 0
    
    # Inisialisasi Root Node
    initial_bound = calculate_bound(candidates, 0, [], k, 0.0)
    root_node = Node(bound=initial_bound, cost=0.0, index=-1, selected=[])
    heapq.heappush(Q, root_node)
    
    while Q:
        node = heapq.heappop(Q)
        nodes_visited += 1 # Integrasi perhitungan statistik node yang dikunjungi
        
        # Pengecekan pada level node orang tua
        is_pruned, _ = prune_branch(
            bound=node.bound,
            current_cost=node.cost,
            B=B,
            best_cost=min_cost,
            slots_needed=k - len(node.selected),
            remaining=len(candidates) - (node.index + 1)
        )
        
        if is_pruned:
            branches_pruned += 1
            continue
            
        # Pengecekan apakah merupakan daun/solusi (memenuhi jumlah anggota k)
        if len(node.selected) == k:
            if node.cost < min_cost:
                best_solution = node.selected
                min_cost = node.cost
            continue
            
        # Pembangkitan anak simpul
        next_idx = node.index + 1
        if next_idx < len(candidates):
            # Cabang 1: Mengambil kandidat berikutnya
            include_candidate = candidates[next_idx]
            new_selected = node.selected + [include_candidate]
            new_cost = node.cost + include_candidate.cost
            
            # Pengecekan kelayakan sebelum memasukkan cabang ini ke dalam antrian
            if new_cost <= B and len(new_selected) <= k:
                bound1 = calculate_bound(candidates, next_idx + 1, new_selected, k, new_cost)
                if bound1 < min_cost:
                    child1 = Node(bound=bound1, cost=new_cost, index=next_idx, selected=new_selected)
                    heapq.heappush(Q, child1)
                else:
                    branches_pruned += 1
            else:
                branches_pruned += 1
                
            # Cabang 2: TIDAK mengambil kandidat berikutnya
            bound2 = calculate_bound(candidates, next_idx + 1, node.selected, k, node.cost)
            # Mengecek apakah jumlah sisa kandidat yang ada masih cukup jika kita tidak mengambil kandidat ini
            if bound2 < min_cost and (len(node.selected) + (len(candidates) - (next_idx + 1)) >= k):
                child2 = Node(bound=bound2, cost=node.cost, index=next_idx, selected=node.selected)
                heapq.heappush(Q, child2)
            else:
                branches_pruned += 1
                
    if min_cost == float('inf'):
        min_cost = 0.0

    return best_solution, min_cost, nodes_visited, branches_pruned


# Representasi simpul (node) dalam pohon pencarian Branch and Bound.
class Node:
    # Konstruktor Node
    # Kamus Lokal
    # index           : Indeks kandidat terakhir yang dipertimbangkan
    # selected        : List kandidat yang sudah dipilih
    # current_cost    : Total biaya kandidat yang dipilih
    # bound           : Lower bound estimasi total biaya
    def __init__(self, bound, cost, index, selected):
        self.bound = bound
        self.cost = cost
        self.index = index
        self.selected = selected
    
    # __lt__()
    # Override metode __lt__ untuk memungkinkan Node disimpan dalam PriorityQueue (min-heap)

    # PriorityQueue akan mengurutkan berdasarkan bound (biaya estimasi terendah)
    def __lt__(self, other):
        return self.bound < other.bound