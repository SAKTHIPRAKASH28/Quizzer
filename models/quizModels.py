from pydantic import BaseModel,Field
from typing import Optional


class QuizGenerationModel(BaseModel):
    topic:str=Field(...,min_length=3)
    no_of_questions:int=Field(...)
    syllabus:Optional[str]=Field(default=None)
    preferences:str=Field(default=None)


class QuizResultModel(BaseModel):
    questionNumber:int=Field(...)
    question:str=Field(...)
    options:dict[str,str]=Field(...)
    correctOption:str=Field(...)


class ModifyQuizRequest(BaseModel):
    quizID: str
    changes: Optional[str] = None
    
class DiscussionWithBotBody(BaseModel):
    text:str
    quizID:str


    
