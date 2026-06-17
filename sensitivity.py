# file: sensitivity.py
# Analisis sensitivitas (what-if) untuk algoritma Branch and Bound.
# Memvariasikan salah satu parameter (anggaran B atau ukuran tim k) pada satu
# rentang nilai, lalu mencatat bagaimana hasil & performa berubah. Logika inti
# B&B TIDAK diubah; modul ini hanya memanggil branch_and_bound berulang kali.

import time
from branch_bound import branch_and_bound

# Batas ukuran tim k (sama dengan validasi di main.py / app.py)
K_MIN, K_MAX = 5, 10


# min_budget_for()
# Menghitung anggaran minimum yang dibutuhkan untuk memilih k kandidat termurah.
# Pola sama dengan validasi di app.py:51 dan main.py:62.
def min_budget_for(candidates: list, k: int) -> float:
    return sum(sorted(c.cost for c in candidates)[:k])


# _solve_point()
# Menjalankan satu kali B&B untuk pasangan (k, B) tertentu dan merangkum hasilnya
# menjadi satu baris (dict). Jika anggaran tidak mencukupi, ditandai infeasible
# tanpa memanggil B&B (konsisten dengan validasi yang ada).
# Kamus Lokal:
# param      : nilai parameter yang sedang divariasikan (B atau k)
# min_budget : anggaran minimum untuk memilih k kandidat termurah (float)
# start/end  : penanda waktu eksekusi (float)
# team ...   : keluaran branch_and_bound
def _solve_point(candidates: list, k: int, B: float, param) -> dict:
    min_budget = min_budget_for(candidates, k)

    # Anggaran tidak mencukupi → tidak ada solusi valid, lewati pemanggilan B&B.
    if B < min_budget:
        return {
            "param": param,
            "feasible": False,
            "total_cost": None,
            "nodes_visited": 0,
            "nodes_generated": 0,
            "pruned_total": 0,
            "exec_time": 0.0,
        }

    start = time.perf_counter()
    team, total_cost, nodes_visited, nodes_generated, prune_stats, _ = \
        branch_and_bound(candidates, k, B)
    exec_time = time.perf_counter() - start

    return {
        "param": param,
        "feasible": bool(team),
        "total_cost": total_cost if team else None,
        "nodes_visited": nodes_visited,
        "nodes_generated": nodes_generated,
        "pruned_total": prune_stats["total"],
        "exec_time": exec_time,
    }


# _frange()
# Menghasilkan deret nilai dari lo sampai hi (inklusif) dengan langkah step.
# Menggunakan integer bila semua input bulat agar label rapi.
def _frange(lo, hi, step):
    if step <= 0:
        raise ValueError("Langkah (step) harus lebih besar dari 0.")
    values = []
    v = lo
    # Toleransi kecil agar batas atas tetap masuk meski ada galat pembulatan float.
    while v <= hi + 1e-9:
        values.append(int(v) if float(v).is_integer() else round(v, 4))
        v += step
    return values


# run_sensitivity()
# Menjalankan analisis sensitivitas dengan memvariasikan B atau k.
# - vary == "B": k tetap, B berjalan dari lo..hi (langkah step)
# - vary == "k": B tetap, k berjalan dari lo..hi (dibatasi K_MIN..K_MAX)
# Mengembalikan list of dict (lihat _solve_point untuk field tiap baris).
# Kamus Lokal:
# rows   : daftar hasil per titik (list of dict)
# k_vals : daftar nilai k yang valid (list)
def run_sensitivity(candidates: list, k: int, B: float, vary: str,
                    lo: float, hi: float, step: float) -> list:
    if vary not in ("B", "k"):
        raise ValueError("Parameter 'vary' harus 'B' atau 'k'.")

    rows = []
    if vary == "B":
        for b_val in _frange(lo, hi, step):
            rows.append(_solve_point(candidates, k, b_val, b_val))
    else:  # vary == "k"
        # Batasi k pada rentang valid 5..10 dan hanya nilai bulat.
        k_lo = max(K_MIN, int(lo))
        k_hi = min(K_MAX, int(hi))
        for k_val in range(k_lo, k_hi + 1):
            rows.append(_solve_point(candidates, k_val, B, k_val))

    return rows


# build_sensitivity_lines()
# Membangun tabel teks hasil sensitivitas sebagai list string (untuk CLI / TXT / PDF),
# bergaya build_stats_lines di utils.py.
# Kamus Lokal:
# header     : judul kolom parameter (string)
# fixed_label: deskripsi parameter yang ditahan tetap (string)
# lines      : daftar baris teks (list of string)
def build_sensitivity_lines(rows: list, vary: str, fixed_label: str) -> list:
    header = "Anggaran (B)" if vary == "B" else "Ukuran tim (k)"
    lines = []
    lines.append("ANALISIS SENSITIVITAS")
    lines.append(f"  Parameter divariasikan     : {header}")
    lines.append(f"  Parameter tetap            : {fixed_label}")
    lines.append("-" * 55)
    lines.append(f"  {header:<14} | {'Total Biaya':>12} | {'Node pop':>9} | {'Waktu (s)':>10}")
    lines.append(f"  {'-' * 51}")
    for r in rows:
        if r["feasible"]:
            cost_str = f"{r['total_cost']:,.0f}"
            time_str = f"{r['exec_time']:.5f}"
            visited_str = f"{r['nodes_visited']:,}"
        else:
            cost_str = "infeasible"
            time_str = "-"
            visited_str = "-"
        lines.append(f"  {str(r['param']):<14} | {cost_str:>12} | {visited_str:>9} | {time_str:>10}")
    lines.append("-" * 55)
    return lines
