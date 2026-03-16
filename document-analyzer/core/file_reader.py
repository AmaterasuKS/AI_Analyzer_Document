from typing import BinaryIO

import fitz  # PyMuPDF
from docx import Document


def read_pdf(file: BinaryIO) -> str:
    """Read a PDF file-like object using PyMuPDF and return extracted text."""
    # PyMuPDF expects a bytes object or a file path, so we read the bytes
    file_bytes = file.read()
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text_parts: list[str] = []
    for page in doc:
        text_parts.append(page.get_text())
    doc.close()
    return "\n".join(text_parts).strip()


def read_docx(file: BinaryIO) -> str:
    """Read a DOCX file-like object using python-docx and return extracted text."""
    # python-docx can open from a file-like object positioned at start
    # поэтому сбросим указатель на начало
    file.seek(0)
    doc = Document(file)
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    return "\n".join(paragraphs).strip()


def read_txt(file: BinaryIO, encoding: str = "utf-8") -> str:
    """Read a plain text file-like object and return text."""
    # Предполагаем, что это бинарный файловый объект (как UploadFile.file)
    file.seek(0)
    content = file.read()
    if isinstance(content, bytes):
        return content.decode(encoding, errors="ignore").strip()
    return str(content).strip()


def get_word_count(text: str) -> int:
    """Return a simple word count for the given text."""
    if not text:
        return 0
    # Простое разбиение по пробелам/переводам строк
    words = text.split()
    return len(words)
