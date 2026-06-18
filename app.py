# file: app.py
# Web server untuk visualisasi algoritma Branch and Bound (pemilihan tim proyek)
# Run Command: python app.py  ->  http://localhost:5000
from flask import Flask, jsonify, render_template, request, send_file

from csv_loader import load_csv
from branch_bound import branch_and_bound
from sensitivity import run_sensitivity
from pdf_export import build_pdf
from utils import build_stats_lines

app = Flask(__name__)

# Daftar dataset yang tersedia (kunci = pilihan dari frontend)
DATASETS = {
    "small": ("datasets/small.csv", "Small"),
    "medium": ("datasets/medium.csv", "Medium"),
    "large": ("datasets/large.csv", "Large"),
}


# parse_request()
# Memvalidasi parameter umum (dataset, k, B) dari body request dan memuat kandidat.
# Mengembalikan tuple (ctx, error_response):
#   ctx            : dict {dataset_name, k, B, candidates} bila valid, else None
#   error_response : tuple (json, status) bila tidak valid, else None
# Dipakai bersama oleh endpoint /api/solve, /api/sensitivity, /api/export/pdf
# agar aturan validasi tetap konsisten (tidak ada duplikasi).
def parse_request(data: dict):
    dataset_key = data.get("dataset")
    if dataset_key not in DATASETS:
        return None, (jsonify(error="Pilihan dataset tidak dikenali."), 400)
    file_path, dataset_name = DATASETS[dataset_key]

    try:
        k = int(data.get("k"))
        B = int(data.get("B"))
    except (TypeError, ValueError):
        return None, (jsonify(error="Input tidak valid! Harap masukkan angka."), 400)
    if not (5 <= k <= 10):
        return None, (jsonify(error="Input tidak valid, input range (5 <= k <= 10)."), 400)

    candidates = load_csv(file_path)
    if not candidates:
        return None, (jsonify(error="Tidak ada data kandidat yang berhasil dimuat."), 500)

    # Validasi budget minimum: B harus cukup untuk k kandidat termurah
    min_budget = sum(sorted(c.cost for c in candidates)[:k])
    if B < min_budget:
        return None, (jsonify(
            error=f"Budget B = {B} tidak mencukupi untuk memilih {k} orang. "
                  f"Minimum budget yang dibutuhkan: {min_budget:.0f}."
        ), 400)

    return {"dataset_name": dataset_name, "k": k, "B": B, "candidates": candidates}, None


# Halaman utama visualisasi
@app.route("/")
def index():
    return render_template("index.html")


# Menjalankan algoritma B&B dan mengembalikan hasil + trace proses sebagai JSON
# Body request: {"dataset": "small|medium|large", "k": int, "B": int}
@app.post("/api/solve")
def solve():
    data = request.get_json(silent=True) or {}
    ctx, err = parse_request(data)
    if err:
        return err
    candidates, k, B = ctx["candidates"], ctx["k"], ctx["B"]

    trace = []
    team, total_cost, nodes_visited, nodes_generated, prune_stats, nodes_popped_and_pruned = \
        branch_and_bound(candidates, k, B, tracer=trace)

    return jsonify(
        dataset=ctx["dataset_name"],
        k=k,
        B=B,
        candidates=[{"id": c.id, "nama": c.nama, "cost": c.cost} for c in candidates],
        team=[{"id": c.id, "nama": c.nama, "cost": c.cost} for c in team],
        total_cost=total_cost,
        stats={
            "nodes_visited": nodes_visited,
            "nodes_generated": nodes_generated,
            "prune_stats": prune_stats,
            "nodes_popped_and_pruned": nodes_popped_and_pruned,
        },
        trace=trace,
    )


# Menjalankan analisis sensitivitas (what-if) dengan memvariasikan B atau k.
# Body request: {dataset, k, B, vary:"B"|"k", lo, hi, step}
@app.post("/api/sensitivity")
def sensitivity():
    data = request.get_json(silent=True) or {}
    ctx, err = parse_request(data)
    if err:
        return err
    candidates, k, B = ctx["candidates"], ctx["k"], ctx["B"]

    vary = data.get("vary", "B")
    if vary not in ("B", "k"):
        return jsonify(error="Parameter 'vary' harus 'B' atau 'k'."), 400
    try:
        lo = float(data.get("lo"))
        hi = float(data.get("hi"))
        step = float(data.get("step"))
    except (TypeError, ValueError):
        return jsonify(error="Rentang analisis (lo/hi/step) tidak valid."), 400
    if step <= 0 or lo > hi:
        return jsonify(error="Rentang analisis tidak valid (pastikan step > 0 dan min <= max)."), 400

    rows = run_sensitivity(candidates, k, B, vary, lo, hi, step)
    fixed_label = f"k = {k}" if vary == "B" else f"B = {B:,.0f}"
    return jsonify(vary=vary, fixed_label=fixed_label, rows=rows)


# Mengekspor hasil pemilihan tim ke berkas PDF (diunduh sebagai attachment).
# Body request: {dataset, k, B, sensitivity?: {vary, fixed_label, rows}}
@app.post("/api/export/pdf")
def export_pdf():
    data = request.get_json(silent=True) or {}
    ctx, err = parse_request(data)
    if err:
        return err
    candidates, k, B = ctx["candidates"], ctx["k"], ctx["B"]

    # Jalankan ulang B&B (tanpa tracer) untuk menyusun hasil & statistik.
    team, total_cost, nodes_visited, nodes_generated, prune_stats, nodes_popped_and_pruned = \
        branch_and_bound(candidates, k, B)

    stats_lines = build_stats_lines(
        len(candidates), k, B, total_cost,
        nodes_visited, nodes_generated, prune_stats,
        exec_time=0.0, nodes_popped_and_pruned=nodes_popped_and_pruned,
    )

    # Sertakan sensitivitas yang dikirim frontend (bila ada).
    sensitivity_data = data.get("sensitivity") or None

    path = build_pdf(
        "hasil_pemilihan.pdf",
        team=team, total_cost=total_cost, k=k, B=B,
        dataset_name=ctx["dataset_name"], stats_lines=stats_lines,
        sensitivity=sensitivity_data,
    )
    return send_file(path, as_attachment=True, download_name="hasil_pemilihan_tim.pdf",
                     mimetype="application/pdf")


if __name__ == "__main__":
    import os
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))
