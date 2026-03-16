# AI Document Analyzer

Веб-приложение для анализа документов (PDF/DOCX/TXT): автоматически делает краткое резюме, выделяет ключевые тезисы и отвечает на вопросы по содержанию.

## Стек

- **Python 3.10+**
- **FastAPI** (backend API)
- **Groq API** (модель: `llama-3.3-70b-versatile`)
- **PyMuPDF** (извлечение текста из PDF)
- **python-docx** (извлечение текста из DOCX)
- **HTML + Tailwind CSS** (frontend, один файл `static/index.html`)

## Возможности

- Загрузка файлов **PDF / DOCX / TXT**
- AI-анализ: **summary** + **key points**
- Q&A: ответ на вопрос по тексту (через endpoint `/question`)

## Скриншот

_TODO: добавить скриншот интерфейса сюда (placeholder)._

## Установка

1) Перейдите в папку проекта:

```bash
cd document-analyzer
```

2) Создайте и активируйте виртуальное окружение:

Windows (PowerShell):

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3) Установите зависимости:

```bash
pip install -r requirements.txt
```

## Настройка переменных окружения

1) Создайте файл `.env` рядом с `main.py`.
2) Добавьте ключ Groq:

```env
GROQ_API_KEY=your_key_here
```

Формат можно посмотреть в `.env.example`.

## Запуск

Из папки `document-analyzer`:

```bash
python main.py
```

После запуска откройте в браузере:

- `http://127.0.0.1:8000/`

## API

- **POST** `/upload` — принимает файл (PDF/DOCX/TXT), возвращает:
  - `filename`
  - `summary`
  - `key_points`
  - `word_count`
- **POST** `/question` — принимает JSON:
  - `question`
  - `document_text`
  и возвращает `answer`

## Примечания

- Для **сканированных PDF** без слоя текста нужен **OCR**, иначе извлечение текста может вернуть пустую строку.

