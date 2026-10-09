from __future__ import annotations

from io import BytesIO
from textwrap import wrap

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from clausewise.models import AnalysisResult


def build_pdf_report(result: AnalysisResult, source_file_name: str) -> bytes:
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    _, height = A4
    y = height - 50

    def draw_line(text: str, font_name: str = 'Helvetica', font_size: int = 11) -> None:
        nonlocal y
        pdf.setFont(font_name, font_size)
        for line in wrap(text, width=95):
            if y < 50:
                pdf.showPage()
                y = height - 50
                pdf.setFont(font_name, font_size)
            pdf.drawString(40, y, line)
            y -= 16

    draw_line('ClauseWise Contract Analysis Report', 'Helvetica-Bold', 16)
    draw_line(f'Source file: {source_file_name}')
    draw_line(f'Risk score: {result.risk_score}/100 ({result.risk_label})')
    draw_line(result.summary)
    draw_line(result.llm_status)
    draw_line('Findings', 'Helvetica-Bold', 13)
    for finding in result.findings:
        draw_line(f'- {finding.title} [{finding.severity}] at {finding.source_reference}')
        draw_line(f'  Matched text: {finding.matched_text}')
    if result.cost_items:
        draw_line('Estimated cost exposure', 'Helvetica-Bold', 13)
        for item in result.cost_items:
            draw_line(f'- {item.label}: ${item.estimated_amount:,.0f}')
        draw_line(f'Total estimated exposure: ${result.total_estimated_cost:,.0f}')
    pdf.save()
    return buffer.getvalue()

