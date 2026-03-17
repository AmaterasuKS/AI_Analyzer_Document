![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-green)
![Groq](https://img.shields.io/badge/Groq-AI-orange)

## How it works

The user uploads a PDF, DOCX, or TXT file through the web interface.
The backend extracts the raw text using PyMuPDF or python-docx depending
on the file type. The extracted text is then sent to the Groq API with
a structured prompt, which returns a concise summary and a list of key
points. Users can also ask specific questions about the document content,
and the AI will answer based strictly on the uploaded text.

# AI Document Analyzer

A web-based document analysis tool (PDF/DOCX/TXT): automatically generates a summary, highlights key points, and answers questions about the content.

## Stack:

- **Python 3.10+**
- **FastAPI** (API backend)
- **Grok API** (model: `llama-3.3-70b-versatile`)
- **PyMuPDF** (text extraction from PDF)
- **python-docx** (text extraction from DOCX)
- **HTML + Tailwind CSS** (frontend, single file `static/index.html`)

## Opportunities:

- Upload **PDF / DOCX / TXT** files
- AI analysis: **summary** + **key points**
- Q&A: answer a question based on the text (via the `/question`)

## Screenshot:

<img width="1900" height="972" alt="image" src="https://github.com/user-attachments/assets/3dc8fcb2-3330-4623-9942-3aec03fed862" />



## Installing:

1) Go to the project folder:

```bash
cd document-analyzer
```

2) Create and activate a virtual environment:

Windows (PowerShell):

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3) Install the dependencies:

```bash
pip install -r requirements.txt
```

## Setting Environment Variables

1) Create a file `.env` next to `main.py`.
2) Add your Grok API-Key:

```env
GROQ_API_KEY=your_key_here
```

You can view the format at `.env.example`.

## Launch

From folder `document-analyzer`:

```bash
python main.py
```

After launching the application, open the following in your browser:

- `http://127.0.0.1:8000/`

## API

- **POST** `/upload` — getting file (PDF/DOCX/TXT), send it back:
  - `filename`
  - `summary`
  - `key_points`
  - `word_count`
- **POST** `/question` — gets JSON:
  - `question`
  - `document_text`
  sending back `answer`

## Notes

- For **scanned PDFs** without a text layer, you need **OCR**; otherwise, text extraction may return an empty string.

