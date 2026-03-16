import os
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse

from core.ai_analyzer import analyze_document, answer_question, GroqNotConfiguredError
from core.file_reader import get_word_count, read_docx, read_pdf, read_pptx, read_txt
from core.models import DocumentResponse, QuestionRequest, QuestionResponse


app = FastAPI(title="AI Document Analyzer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"


def _detect_extension(filename: str | None) -> Literal["pdf", "docx", "pptx", "txt"] | None:
    if not filename:
        return None
    ext = filename.lower().rsplit(".", 1)[-1]
    if ext in {"pdf", "docx", "pptx", "txt"}:
        return ext  # type: ignore[return-value]
    return None


@app.post("/upload", response_model=DocumentResponse)
async def upload_document(file: UploadFile = File(...)) -> DocumentResponse:
    ext = _detect_extension(file.filename)
    if ext is None:
        raise HTTPException(
            status_code=400,
            detail="Поддерживаются только файлы PDF, DOCX, PPTX и TXT.",
        )

    try:
        if ext == "pdf":
            text = read_pdf(file.file)
        elif ext == "docx":
            text = read_docx(file.file)
        elif ext == "pptx":
            text = read_pptx(file.file)
        else:
            text = read_txt(file.file)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка чтения файла: {e}",
        ) from e

    if not text.strip():
        raise HTTPException(
            status_code=400,
            detail="Не удалось извлечь текст из документа.",
        )

    try:
        summary, key_points = analyze_document(text)
    except GroqNotConfiguredError as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка анализа документа ИИ: {e}",
        ) from e

    word_count = get_word_count(text)

    return DocumentResponse(
        filename=file.filename or "document",
        summary=summary,
        key_points=key_points,
        word_count=word_count,
        document_text=text,
    )


@app.post("/question", response_model=QuestionResponse)
async def ask_question(payload: QuestionRequest) -> QuestionResponse:
    if not payload.document_text.strip():
        raise HTTPException(
            status_code=400,
            detail="Текст документа пустой.",
        )
    if not payload.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Вопрос не может быть пустым.",
        )

    try:
        answer = answer_question(
            question=payload.question,
            document_text=payload.document_text,
        )
    except GroqNotConfiguredError as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка ответа ИИ на вопрос: {e}",
        ) from e

    return QuestionResponse(answer=answer)


@app.get("/", response_class=HTMLResponse)
async def serve_index() -> HTMLResponse:
    index_path = STATIC_DIR / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="index.html не найден.")
    # FastAPI вернёт корректный Content-Type для HTMLResponse
    return HTMLResponse(index_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        reload=True,
    )

