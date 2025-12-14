from pathlib import Path
import fitz  # PyMuPDF


def extract_text_from_pdf(pdf_path: Path) -> str:
    doc = fitz.open(pdf_path)
    text = []

    for page in doc:
        text.append(page.get_text())

    return "\n".join(text)
