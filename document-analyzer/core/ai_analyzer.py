import json
import os
from typing import List, Tuple

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = "llama-3.3-70b-versatile"

client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None


class GroqNotConfiguredError(RuntimeError):
    pass


def _ensure_client() -> Groq:
    if client is None:
        raise GroqNotConfiguredError(
            "GROQ_API_KEY is not set. Please configure it in your .env file."
        )
    return client


def analyze_document(text: str) -> Tuple[str, List[str]]:
    """
    Analyze document text using Groq and return (summary, key_points).
    """
    groq_client = _ensure_client()

    prompt = (
        "You are an AI assistant that summarizes documents in Russian.\n"
        "Given the following document text, provide:\n"
        "1) A concise summary (3–5 sentences).\n"
        "2) 5–10 key bullet points capturing the most important facts.\n\n"
        "Return your response strictly in the following JSON format:\n"
        '{\n'
        '  \"summary\": \"...\",\n'
        '  \"key_points\": [\"...\", \"...\", \"...\"]\n'
        "}\n\n"
        "Document text:\n"
        f"{text}\n"
    )

    response = groq_client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful AI assistant for document analysis.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    content = response.choices[0].message.content or ""

    # Убираем markdown-обёртку ```json ... ``` или ``` ... ```, если есть
    text = content.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines)

    # Попробуем распарсить JSON-ответ, но при ошибке вернём всё как один summary.
    try:
        data = json.loads(text)
        summary = str(data.get("summary", "")).strip()
        raw_points = data.get("key_points", [])
        key_points = [str(p).strip() for p in raw_points if str(p).strip()]
        if not key_points:
            key_points = [summary] if summary else []
    except json.JSONDecodeError:
        summary = content.strip()
        key_points = [summary] if summary else []

    return summary, key_points


def answer_question(question: str, document_text: str) -> str:
    """
    Answer a question based on the given document text using Groq.
    """
    groq_client = _ensure_client()

    prompt = (
        "You are an AI assistant that answers questions based on a provided document.\n"
        "Always answer in Russian and rely only on the given document text.\n"
        "If the answer cannot be found in the document, say that the document "
        "does not contain enough information.\n\n"
        "Document text:\n"
        f"{document_text}\n\n"
        f"Question: {question}\n"
    )

    response = groq_client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful AI assistant for document Q&A.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    content = response.choices[0].message.content or ""
    return content.strip()

