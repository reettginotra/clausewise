from __future__ import annotations

from io import BytesIO
from pathlib import Path

import fitz
from docx import Document

from clausewise.models import TextSegment


class UnsupportedFileTypeError(ValueError):
    pass


def extract_document_bytes(file_name: str, file_bytes: bytes) -> list[TextSegment]:
    suffix = Path(file_name).suffix.lower()
    if suffix == '.pdf':
        return _extract_pdf(file_name, file_bytes)
    if suffix == '.docx':
        return _extract_docx(file_name, file_bytes)
    if suffix == '.txt':
        return _extract_txt(file_name, file_bytes)
    suffix_label = suffix or 'unknown'
    raise UnsupportedFileTypeError(f'Unsupported file type: {suffix_label}')


def _extract_pdf(file_name: str, file_bytes: bytes) -> list[TextSegment]:
    segments: list[TextSegment] = []
    document = fitz.open(stream=file_bytes, filetype='pdf')
    try:
        for page_number, page in enumerate(document, start=1):
            text = page.get_text('text').strip()
            if text:
                segments.append(TextSegment('pdf', file_name, text, f'Page {page_number}'))
    finally:
        document.close()
    return segments


def _extract_docx(file_name: str, file_bytes: bytes) -> list[TextSegment]:
    document = Document(BytesIO(file_bytes))
    segments: list[TextSegment] = []
    for paragraph_number, paragraph in enumerate(document.paragraphs, start=1):
        text = paragraph.text.strip()
        if text:
            segments.append(TextSegment('docx', file_name, text, f'Paragraph {paragraph_number}'))
    return segments


def _extract_txt(file_name: str, file_bytes: bytes) -> list[TextSegment]:
    segments: list[TextSegment] = []
    for line_number, line in enumerate(file_bytes.decode('utf-8', errors='ignore').splitlines(), start=1):
        cleaned = line.strip()
        if cleaned:
            segments.append(TextSegment('txt', file_name, cleaned, f'Line {line_number}'))
    return segments

