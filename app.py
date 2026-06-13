# file: app.py
# Web server untuk visualisasi algoritma Branch and Bound (pemilihan tim proyek)
# Run Command: python app.py  ->  http://localhost:5000
from flask import Flask, jsonify, render_template, request

from csv_loader import load_csv
from branch_bound import branch_and_bound

app = Flask(__name__)

# Daftar dataset yang tersedia (kunci = pilihan dari frontend)
DATASETS = {
    "small": ("datasets/small.csv", "Small"),
    "medium": ("datasets/medium.csv", "Medium"),
    "large": ("datasets/large.csv", "Large"),
}


# Halaman utama visualisasi
@app.route("/")
def index():
    return render_template("index.html")


# Menjalankan algoritma B&B dan mengembalikan hasil + trace proses sebagai JSON
# Body request: {"dataset": "small|medium|large", "k": int, "B": int}
@app.post("/api/solve")
def solve():
    data = request.get_json(silent=True) or {}

    # Validasi dataset
    dataset_key = data.get("dataset")
    if dataset_key not in DATASETS:
        return jsonify(error="Pilihan dataset tidak dikenali."), 400
    file_path, dataset_name = DATASETS[dataset_key]

    # Validasi k dan B (aturan sama dengan CLI di main.py)
    try:
        k = int(data.get("k"))
        B = int(data.get("B"))
    except (TypeError, ValueError):
        return jsonify(error="Input tidak valid! Harap masukkan angka."), 400
    if not (5 <= k <= 10):
        return jsonify(error="Input tidak valid, input range (5 <= k <= 10)."), 400

    candidates = load_csv(file_path)
    if not candidates:
        return jsonify(error="Tidak ada data kandidat yang berhasil dimuat."), 500

    # Validasi budget minimum: B harus cukup untuk k kandidat termurah
    min_budget = sum(sorted(c.cost for c in candidates)[:k])
    if B < min_budget:
        return jsonify(
            error=f"Budget B = {B} tidak mencukupi untuk memilih {k} orang. "
                  f"Minimum budget yang dibutuhkan: {min_budget:.0f}."
        ), 400

    trace = []
    team, total_cost, nodes_visited, nodes_generated, prune_stats, nodes_popped_and_pruned = \
        branch_and_bound(candidates, k, B, tracer=trace)

    return jsonify(
        dataset=dataset_name,
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


if __name__ == "__main__":
    import os
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))
