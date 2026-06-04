%% Flowchart Branch and Bound (Mermaid)
graph TD
    Start([Start]) --> Init[Inisialisasi:<br>1. Urutkan kandidat berdasarkan cost asc<br>2. min_cost = INFINITY<br>3. best_solution = NULL<br>4. Q = PriorityQueue]
    Init --> PushRoot[Masukkan RootNode ke Q]
    PushRoot --> CheckQ{Apakah Q kosong?}
    
    CheckQ -- Ya --> End([Selesai:<br>Kembalikan best_solution & statistik])
    CheckQ -- Tidak --> Dequeue[Ambil node dengan bound terkecil dari Q]
    
    Dequeue --> PruneCheck{Apakah node.bound >= min_cost<br>ATAU node.current_cost > B?}
    PruneCheck -- Ya --> Prune[Pangkas Cabang<br>branches_pruned++]
    Prune --> CheckQ
    
    PruneCheck -- Tidak --> CheckK{Apakah jumlah anggota == k?}
    
    CheckK -- Ya --> CheckMin{Apakah node.current_cost < min_cost?}
    CheckMin -- Ya --> UpdateBest[Update best_solution = node.selected<br>min_cost = node.current_cost]
    UpdateBest --> CheckQ
    CheckMin -- Tidak --> CheckQ
    
    CheckK -- Tidak --> GenerateChildren[Bangkitkan anak simpul:<br>1. Cabang Baru dengan kandidat berikutnya<br>2. Cabang Baru tanpa kandidat berikutnya]
    GenerateChildren --> CalcBound[Hitung bound untuk setiap anak]
    CalcBound --> PushChildren[Masukkan anak yang memenuhi syarat ke dalam Q]
    PushChildren --> CheckQ