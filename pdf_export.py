# file: pdf_export.py
# Ekspor hasil pemilihan tim (Branch and Bound) ke berkas PDF ringkasan.
# Memakai reportlab (pure-Python). Berisi: parameter, tabel tim terpilih,
# statistik B&B, dan — bila tersedia — tabel + grafik analisis sensitivitas.

import os

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Preformatted,
)
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.linecharts import HorizontalLineChart

# Palet warna selaras dengan tema web (index.html)
ACCENT = colors.HexColor("#534AB7")
ACCENT_DARK = colors.HexColor("#26215C")
HEAD_BG = colors.HexColor("#534AB7")
ROW_ALT = colors.HexColor("#f1efe8")
LINE_GREY = colors.HexColor("#e0ded6")


# _unique_export_path()
# Mengembalikan path unik di dalam folder 'exports' (pola sama dengan export_to_txt).
def _unique_export_path(file_name: str) -> str:
    os.makedirs("exports", exist_ok=True)
    base, ext = os.path.splitext(os.path.basename(file_name))
    if ext.lower() != ".pdf":
        ext = ".pdf"
    target = os.path.join("exports", base + ext)
    counter = 2
    while os.path.exists(target):
        target = os.path.join("exports", f"{base}_{counter}{ext}")
        counter += 1
    return target


# _member_fields()
# Mengambil (id, nama, cost) dari anggota tim, mendukung objek Candidate maupun dict.
def _member_fields(m):
    if isinstance(m, dict):
        return m.get("id", ""), m.get("nama", ""), m.get("cost", 0)
    return m.id, m.nama, m.cost


# _team_table()
# Membangun tabel "Tim Terpilih" sebagai Flowable platypus.
def _team_table(team, total_cost):
    data = [["No", "ID", "Nama Kandidat", "Cost"]]
    for i, member in enumerate(team, start=1):
        mid, nama, cost = _member_fields(member)
        data.append([str(i), str(mid), str(nama), f"{cost:,.0f}"])
    data.append(["", "", "Total Biaya", f"{total_cost:,.0f}"])

    table = Table(data, colWidths=[1.2 * cm, 2.2 * cm, 8.5 * cm, 3.5 * cm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HEAD_BG),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (3, 0), (3, -1), "RIGHT"),
        ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -2), [colors.white, ROW_ALT]),
        ("LINEBELOW", (0, 0), (-1, -2), 0.4, LINE_GREY),
        ("LINEABOVE", (0, -1), (-1, -1), 0.8, ACCENT),
        ("FONTNAME", (2, -1), (-1, -1), "Helvetica-Bold"),
        ("TEXTCOLOR", (2, -1), (-1, -1), ACCENT_DARK),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return table


# _sensitivity_table()
# Membangun tabel ringkas hasil sensitivitas.
def _sensitivity_table(rows, header):
    data = [[header, "Total Biaya", "Node pop", "Waktu (s)"]]
    for r in rows:
        if r["feasible"]:
            data.append([str(r["param"]), f"{r['total_cost']:,.0f}",
                         f"{r['nodes_visited']:,}", f"{r['exec_time']:.5f}"])
        else:
            data.append([str(r["param"]), "infeasible", "-", "-"])

    table = Table(data, colWidths=[4 * cm, 4 * cm, 3.5 * cm, 3.5 * cm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HEAD_BG),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, ROW_ALT]),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, LINE_GREY),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return table


# _line_chart()
# Membuat grafik garis satu deret (Drawing) dari pasangan (label, nilai).
# Titik infeasible (nilai None) dilewati.
def _line_chart(labels, values, color, value_fmt="{:.0f}"):
    drawing = Drawing(440, 180)
    chart = HorizontalLineChart()
    chart.x = 45
    chart.y = 30
    chart.width = 370
    chart.height = 125
    chart.data = [values]
    chart.lines[0].strokeColor = color
    chart.lines[0].strokeWidth = 2
    chart.categoryAxis.categoryNames = [str(l) for l in labels]
    chart.categoryAxis.labels.fontSize = 7
    chart.categoryAxis.labels.angle = 30
    chart.categoryAxis.labels.boxAnchor = "ne"
    chart.valueAxis.labels.fontSize = 7
    valid = [v for v in values if v is not None]
    if valid:
        chart.valueAxis.valueMin = min(valid) * 0.95
        chart.valueAxis.valueMax = max(valid) * 1.05 if max(valid) > 0 else 1
    drawing.add(chart)
    return drawing


# build_pdf()
# Membangun berkas PDF ringkasan hasil dan mengembalikan path final.
# Argumen:
#   out_path      : nama berkas (akan dibuat unik di folder exports/)
#   team          : daftar anggota tim (objek Candidate atau dict)
#   total_cost    : total biaya tim terpilih
#   k, B          : parameter pemilihan
#   dataset_name  : nama dataset (opsional)
#   stats_lines   : list string statistik (hasil build_stats_lines di utils.py)
#   sensitivity   : opsional dict {"vary","fixed_label","rows"} dari run_sensitivity
def build_pdf(out_path, *, team, total_cost, k, B, dataset_name=None,
              stats_lines=None, sensitivity=None) -> str:
    target = _unique_export_path(out_path)

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("TitleX", parent=styles["Title"],
                                 textColor=ACCENT_DARK, fontSize=18, spaceAfter=4)
    h2 = ParagraphStyle("H2X", parent=styles["Heading2"],
                        textColor=ACCENT, fontSize=12, spaceBefore=14, spaceAfter=6)
    body = styles["BodyText"]
    mono = ParagraphStyle("MonoX", parent=styles["Code"], fontSize=8, leading=11)

    story = [
        Paragraph("Hasil Pemilihan Tim Proyek", title_style),
        Paragraph("Metode: Branch &amp; Bound", body),
        Spacer(1, 6),
    ]

    # Parameter
    params = f"<b>Target anggota (k):</b> {k} &nbsp;&nbsp; <b>Batas anggaran (B):</b> {B:,.0f}"
    if dataset_name:
        params += f" &nbsp;&nbsp; <b>Dataset:</b> {dataset_name}"
    story.append(Paragraph(params, body))

    # Tim terpilih
    story.append(Paragraph("Tim Terpilih", h2))
    if team:
        story.append(_team_table(team, total_cost))
    else:
        story.append(Paragraph("Tidak ada kombinasi tim yang memenuhi kriteria.", body))

    # Statistik B&B
    if stats_lines:
        story.append(Paragraph("Statistik Branch &amp; Bound", h2))
        story.append(Preformatted("\n".join(stats_lines), mono))

    # Analisis sensitivitas (opsional)
    if sensitivity and sensitivity.get("rows"):
        rows = sensitivity["rows"]
        vary = sensitivity.get("vary", "B")
        header = "Anggaran (B)" if vary == "B" else "Ukuran tim (k)"
        story.append(Paragraph("Analisis Sensitivitas", h2))
        fixed_label = sensitivity.get("fixed_label", "")
        if fixed_label:
            story.append(Paragraph(f"Parameter tetap: {fixed_label}", body))
        story.append(Spacer(1, 4))
        story.append(_sensitivity_table(rows, header))

        labels = [r["param"] for r in rows]
        cost_vals = [r["total_cost"] if r["feasible"] else None for r in rows]
        node_vals = [r["nodes_visited"] for r in rows]

        story.append(Spacer(1, 8))
        story.append(Paragraph("Total biaya vs " + header, body))
        story.append(_line_chart(labels, cost_vals, colors.HexColor("#0F6E56")))
        story.append(Paragraph("Node dikunjungi (pop) vs " + header, body))
        story.append(_line_chart(labels, node_vals, ACCENT))

    doc = SimpleDocTemplate(target, pagesize=A4,
                            leftMargin=2 * cm, rightMargin=2 * cm,
                            topMargin=2 * cm, bottomMargin=2 * cm,
                            title="Hasil Pemilihan Tim Proyek")
    doc.build(story)
    return target
