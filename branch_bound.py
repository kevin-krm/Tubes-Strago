# file: branch_bound.py
# Implementasi algoritma Branch and Bound untuk pemilihan tim proyek

import heapq

# calculate_bound()
# Menghitung estimasi lower bound dari suatu node dalam pohon pencarian Branch and Bound

# Kamus Lokal:
# candidates      : daftar kandidat yang sudah diurutkan berdasarkan cost (list)
# start_index     : indeks kandidat pertama yang masih tersedia (integer)
# selected_count  : jumlah kandidat yang sudah dipilih (integer)
# k               : jumlah anggota tim yang harus dipenuhi (integer)
# current_cost    : total biaya sementara (float)
# n               : jumlah total kandidat (integer)
# slots_needed    : jumlah slot anggota tim yang masih dibutuhkan (integer)
# remaining_count : jumlah kandidat yang masih tersedia (integer)
# bound           : nilai lower bound biaya minimum (float)
# i               : counter (integer)
def calculate_bound(candidates: list, start_index: int, selected_count: int, k: int, current_cost: float, n: int) -> float:
    slots_needed = k - selected_count
    # Jika tidak ada slot lagi yang dibutuhkan, bound = current_cost
    if slots_needed == 0:
        return current_cost
    # Hitung jumlah kandidat tersisa tanpa membuat list baru (optimasi: hindari slicing)
    remaining_count = n - start_index
    # Jika kandidat tersisa kurang dari slot yang masih dibutuhkan, state ini tidak mungkin menghasilkan solusi valid (bound = inf)
    if remaining_count < slots_needed:
        return float('inf')
    # Tambahkan cost dari 'slots_needed' kandidat termurah yang tersisa (list sudah terurut, jadi ambil elemen pertama)
    # Optimasi: akses langsung via index arithmetic, tanpa alokasi list baru
    bound = current_cost
    for i in range(slots_needed):
        bound += candidates[start_index + i].cost

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
    # Jika biaya sudah melebihi anggaran atau estimasi terendah melebihi anggaran, pangkas cabang
    if current_cost > B or bound > B:
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
# Parameter tracer (opsional): list yang akan diisi event proses pencarian
# (push/pop/prune/incumbent) untuk keperluan visualisasi; None = tanpa perekaman.
def branch_and_bound(candidates: list, k: int, B: float, tracer: list = None):
    # Mengurutkan kandidat berdasarkan cost dari yang termurah (Least Cost Search)
    candidates.sort(key=lambda x: x.cost)
    n = len(candidates)  # Simpan sekali, hindari pemanggilan len() berulang
    
    Q = [] # Priority Queue
    best_solution = ()
    min_cost = float('inf')
    nodes_visited = 0
    nodes_generated = 0

    # Statistik pruning per alasan
    prune_stats = {
        "budget": 0,       # Dipangkas karena melebihi anggaran
        "bound": 0,        # Dipangkas karena bound >= best_cost
        "feasibility": 0,  # Dipangkas karena kandidat sisa tidak cukup
        "total": 0         # Total cabang dipangkas
    }
    nodes_popped_and_pruned = 0
    node_counter = 0  # ID unik per node yang dibangkitkan (root = 0), untuk tracer

    # trace()
    # Mencatat satu event proses pencarian ke tracer (jika tracer aktif)
    def trace(**event):
        if tracer is not None:
            tracer.append(event)

    # consider_child()
    # Mengevaluasi satu cabang anak: SELALU menaikkan nodes_generated (baik anak
    # di-push maupun dipangkas saat lahir), lalu memutuskan push/prune dengan
    # urutan alasan yang konsisten: feasibility -> budget -> bound.
    # Ini menyatukan logika pruning kedua cabang (ambil/tidak ambil) di satu tempat
    # sehingga statistik node tetap konsisten (total_pruned <= nodes_generated).
    # Kamus Lokal:
    # child_cost     : total biaya cabang anak (float)
    # child_selected : tuple kandidat terpilih pada anak (tuple)
    # child_index    : indeks kandidat terakhir yang dipertimbangkan (integer)
    # child_count    : jumlah kandidat terpilih pada anak (integer)
    # slots_needed   : slot anggota yang masih dibutuhkan (integer)
    # remaining      : jumlah kandidat yang masih tersedia setelah child_index (integer)
    # child_bound    : lower bound cabang anak (float)
    # parent_id      : ID node induk untuk pencatatan tracer (integer)
    # branch         : label cabang 'include'/'exclude' untuk tracer (string)
    def consider_child(child_cost, child_selected, child_index, child_count, parent_id, branch):
        nonlocal nodes_generated, node_counter
        nodes_generated += 1
        node_counter += 1
        child_id = node_counter

        slots_needed = k - child_count
        remaining = n - (child_index + 1)

        # prune_child()
        # Mencatat pemangkasan anak ke statistik dan tracer dengan alasan tertentu
        def prune_child(reason, child_bound=None):
            prune_stats[reason] += 1
            prune_stats["total"] += 1
            trace(type="node", id=child_id, parent=parent_id, branch=branch,
                  cost=child_cost, bound=child_bound, status="pruned", reason=reason,
                  selected=[c.id for c in child_selected])

        # Feasibility: kandidat tersisa tidak cukup untuk memenuhi kuota k
        if remaining < slots_needed:
            prune_child("feasibility")
            return
        # Budget: biaya parsial sudah melebihi anggaran
        if child_cost > B:
            prune_child("budget")
            return
        # Budget: estimasi terendah (bound) melebihi anggaran
        child_bound = calculate_bound(candidates, child_index + 1, child_count, k, child_cost, n)
        if child_bound > B:
            prune_child("budget", child_bound)
            return
        # Bound: estimasi terendah tidak lebih baik dari solusi terbaik saat ini
        if child_bound >= min_cost:
            prune_child("bound", child_bound)
            return
        # Cabang layak: masukkan ke priority queue
        heapq.heappush(Q, Node(bound=child_bound, cost=child_cost, index=child_index,
                               selected=child_selected, node_id=child_id))
        trace(type="node", id=child_id, parent=parent_id, branch=branch,
              cost=child_cost, bound=child_bound, status="pushed",
              selected=[c.id for c in child_selected])

    # Inisialisasi Root Node (selected sebagai tuple untuk efisiensi memori)
    initial_bound = calculate_bound(candidates, 0, 0, k, 0.0, n)
    root_node = Node(bound=initial_bound, cost=0.0, index=-1, selected=(), node_id=0)
    heapq.heappush(Q, root_node)
    nodes_generated += 1
    trace(type="node", id=0, parent=None, branch="root",
          cost=0.0, bound=initial_bound, status="pushed", selected=[])

    while Q:
        node = heapq.heappop(Q)
        nodes_visited += 1 # Integrasi perhitungan statistik node yang dikunjungi
        trace(type="pop", id=node.node_id, bound=node.bound, cost=node.cost)

        selected_count = len(node.selected)

        # Pengecekan pada level node orang tua
        is_pruned, reason = prune_branch(
            bound=node.bound,
            current_cost=node.cost,
            B=B,
            best_cost=min_cost,
            slots_needed=k - selected_count,
            remaining=n - (node.index + 1)
        )

        if is_pruned:
            prune_stats[reason] += 1
            prune_stats["total"] += 1
            nodes_popped_and_pruned += 1
            trace(type="prune_pop", id=node.node_id, reason=reason)
            continue

        # Pengecekan apakah merupakan daun/solusi (memenuhi jumlah anggota k)
        if selected_count == k:
            if node.cost < min_cost:
                best_solution = node.selected
                min_cost = node.cost
                trace(type="incumbent", id=node.node_id, cost=node.cost,
                      selected=[c.id for c in node.selected])
            continue
            
        # Pembangkitan anak simpul (binary branching pada kandidat berikutnya)
        next_idx = node.index + 1
        if next_idx < n:
            include_candidate = candidates[next_idx]

            # Cabang 1: MENGAMBIL kandidat berikutnya
            consider_child(
                node.cost + include_candidate.cost,
                node.selected + (include_candidate,),  # Tuple concat (lebih efisien dari list)
                next_idx,
                selected_count + 1,
                node.node_id,
                "include",
            )

            # Cabang 2: TIDAK mengambil kandidat berikutnya
            consider_child(
                node.cost,
                node.selected,
                next_idx,
                selected_count,
                node.node_id,
                "exclude",
            )

    if min_cost == float('inf'):
        min_cost = 0.0

    return list(best_solution), min_cost, nodes_visited, nodes_generated, prune_stats, nodes_popped_and_pruned


# Representasi simpul (node) dalam pohon pencarian Branch and Bound.
class Node:
    __slots__ = ('bound', 'cost', 'index', 'selected', 'node_id')

    # Konstruktor Node
    # Kamus Lokal
    # index           : Indeks kandidat terakhir yang dipertimbangkan
    # selected        : Tuple kandidat yang sudah dipilih
    # current_cost    : Total biaya kandidat yang dipilih
    # bound           : Lower bound estimasi total biaya
    # node_id         : ID unik node untuk pencatatan tracer/visualisasi
    def __init__(self, bound, cost, index, selected, node_id=0):
        self.bound = bound
        self.cost = cost
        self.index = index
        self.selected = selected
        self.node_id = node_id
    
    # __lt__()
    # Override metode __lt__ untuk memungkinkan Node disimpan dalam PriorityQueue (min-heap)

    # PriorityQueue akan mengurutkan berdasarkan bound (biaya estimasi terendah)
    def __lt__(self, other):
        return self.bound < other.bound