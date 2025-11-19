import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

import matplotlib.pyplot as plt

def generate_pdf_report(input_text, similarities, highlights):
    pdf_path = "luxury_report.pdf"

    # Pie chart
    labels = [s["doc"] for s in similarities]
    values = [s["score"] * 100 for s in similarities]

    if sum(values) == 0:
        values = [1] * len(labels)

    plt.figure(figsize=(4, 4))
    plt.pie(values, labels=labels, autopct="%1.1f%%")
    plt.title("Similarity Distribution")
    chart_path = "chart.png"
    plt.savefig(chart_path, dpi=180, bbox_inches="tight")
    plt.close()

    styles = getSampleStyleSheet()
    gold_title = ParagraphStyle(
        "GoldTitle",
        parent=styles["Title"],
        textColor=colors.HexColor("#C6A667"),
        fontSize=26,
        spaceAfter=20,
    )
    gold_sub = ParagraphStyle(
        "GoldSub",
        parent=styles["Heading2"],
        textColor=colors.HexColor("#D4AF37"),
        fontSize=18,
        spaceAfter=10,
    )

    normal = styles["Normal"]

    story = []

    story.append(Paragraph("📘 Premium Plagiarism Report", gold_title))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Your Input</b>", gold_sub))
    story.append(Paragraph(input_text.replace("\n", "<br/>"), normal))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Overall Similarity Scores</b>", gold_sub))

    table_data = [["Document", "Score (%)"]]
    for s in similarities:
        table_data.append([s["doc"], round(s["score"] * 100, 2)])

    table = Table(table_data, colWidths=[200, 100])
    table.setStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#C6A667")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#F9F5E7")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ])
    story.append(table)
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Similarity Pie Chart</b>", gold_sub))
    story.append(Image(chart_path, width=300, height=300))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Exact Highlight Matches</b>", gold_sub))

    for h in highlights:
        story.append(Paragraph(f"<b>{h['doc']}</b> — {round(h['score'] * 100, 2)}%", normal))
        story.append(Paragraph(h["highlighted"].replace("\n", "<br/>"), normal))
        story.append(Spacer(1, 12))

    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    doc.build(story)

    return pdf_path
