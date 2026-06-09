# file: utils.py
import time
from functools import wraps

# Decorator untuk menghitung dan mencetak waktu eksekusi sebuah fungsi
def execution_timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        return result, execution_time
    return wrapper

# Mencetak header yang rapih
def print_header(title):
    print("\n" + "=" * 50)
    print(f"{title.center(50)}")
    print("=" * 50)

# Format pencetakan output akhir sesuai rancangan
def display_result(team, total_cost, k, B, nodes_visited, nodes_generated, prune_stats, nodes_popped_and_pruned, exec_time):
    print_header("HASIL PEMILIHAN TIM PROYEK")
    
    if not team:
        print("Tidak ada kombinasi tim yang memenuhi kriteria.")
    else:
        print(f"Target Anggota Tim (k) : {k} orang")
        print(f"Batas Anggaran (B)     : {B}\n")
        
        print("Daftar Anggota Tim Terpilih:")
        for i, member in enumerate(team, start=1):
            print(f"  {i}. {member.nama} (ID: {member.id}, Cost: {member.cost})")
        
        print("-" * 50)
        print(f"Total Biaya Tim        : {total_cost}")
    
    print_header("STATISTIK BRANCH & BOUND")
    print(f"Node dikunjungi        : {nodes_visited}")
    print(f"Cabang dipangkas       : {prune_stats['total']}")
    print(f"Waktu eksekusi         : {exec_time:.5f} detik")
    print("=" * 50 + "\n")

# Fungsi untuk mengekspor hasil pemilihan tim dan statistik pencarian ke berkas TXT
def export_to_txt(file_path, team, total_cost, k, B, nodes_visited, nodes_generated, prune_stats, nodes_popped_and_pruned, exec_time):
    import os
    # Membuat folder 'exports' jika belum ada
    os.makedirs("exports", exist_ok=True)
    
    # Path file tujuan berada di dalam folder 'exports'
    target_path = os.path.join("exports", os.path.basename(file_path))
    
    try:
        with open(target_path, mode='w', encoding='utf-8') as f:
            f.write("=" * 50 + "\n")
            f.write(f"{'HASIL PEMILIHAN TIM PROYEK'.center(50)}\n")
            f.write("=" * 50 + "\n")
            
            if not team:
                f.write("Tidak ada kombinasi tim yang memenuhi kriteria.\n")
            else:
                f.write(f"Target Anggota Tim (k) : {k} orang\n")
                f.write(f"Batas Anggaran (B)     : {B}\n\n")
                
                f.write("Daftar Anggota Tim Terpilih:\n")
                for i, member in enumerate(team, start=1):
                    f.write(f"  {i}. {member.nama} (ID: {member.id}, Cost: {member.cost})\n")
                
                f.write("-" * 50 + "\n")
                f.write(f"Total Biaya Tim        : {total_cost}\n")
            
            f.write("\n" + "=" * 50 + "\n")
            f.write(f"{'STATISTIK BRANCH & BOUND'.center(50)}\n")
            f.write("=" * 50 + "\n")
            f.write(f"Node dikunjungi          : {nodes_visited}\n")
            f.write(f"Cabang dipangkas         : {prune_stats['total']}\n")
            f.write(f"Waktu eksekusi           : {exec_time:.5f} detik\n")
            f.write("=" * 50 + "\n")
        return True, target_path
    except Exception as e:
        print(f"[Error] Gagal mengekspor hasil ke berkas TXT: {e}")
        return False, ""