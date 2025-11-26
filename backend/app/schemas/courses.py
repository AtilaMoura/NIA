from pydantic import BaseModel
from typing import List, Optional

class CourseGenerateRequest(BaseModel):
    topic: str
    goal: str
    level: str = "beginner"
    num_modules: int = 3
    quizzes: bool = True
 

class Module(BaseModel):
    topic: str
    content: str
    quiz: Optional[List[str]] = None


class CourseGenerateResponse(BaseModel):
    topic: str
    summary: str
    modules: List[Module]
