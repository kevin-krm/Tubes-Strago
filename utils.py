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
def display_result(team, total_cost, k, B, nodes, pruned, exec_time):
    print_header("HASIL PEMILIHAN TIM PROYEK")
    
    if not team:
        print("Tidak ada kombinasi tim yang memenuhi kriteria.")
    else:
        print(f"Target Anggota Tim (k) : {k} orang")
        print(f"Batas Anggaran (B)     : {B}\n")
        
        print("Daftar Anggota Tim Terpilih:")
        for i, member in enumerate(team, start=1):
            print(f"  {i}. {member.nama} (Cost: {member.cost})")
        
        print("-" * 50)
        print(f"Total Biaya Tim        : {total_cost}")
    
    print_header("STATISTIK BRANCH & BOUND")
    print(f"Node dikunjungi        : {nodes}")
    print(f"Cabang dipangkas       : {pruned}")
    print(f"Waktu eksekusi         : {exec_time:.5f} detik")
    print("=" * 50 + "\n")