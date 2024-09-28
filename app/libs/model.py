from typing import List, Optional
from pydantic import BaseModel, Field


class Question(BaseModel):
    question: Optional[str] = Field(...,
                                    description="The text of the question")
    options: Optional[List[str]] = Field(...,
                                         description="The available options for the question")
    answer: Optional[str] = Field(...,
                                  description="The correct answer for the question")
    explanation: Optional[str] = Field(...,
                                       description="The explanation for the answer")
    question_category: Optional[str] = Field(...,
                                             description="The category of the question")


class QuestionList(BaseModel):
    questions: List[Question]


class Request(BaseModel):
    body: str
