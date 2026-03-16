from pydantic import BaseModel


class DocumentResponse(BaseModel):
    filename: str
    summary: str
    key_points: list[str]
    word_count: int


class QuestionRequest(BaseModel):
    question: str
    document_text: str


class QuestionResponse(BaseModel):
    answer: str
