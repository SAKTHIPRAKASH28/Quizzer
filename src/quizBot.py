from fastapi.routing import APIRouter
from fastapi.requests import Request
from sqlalchemy import select
from database.quizStorage import addQuiz,getQuiz
from database.historyStorage import *
from fastapi import Body,Query,Depends
from sqlalchemy.orm import Session
from database.quizData import get_db,QuizData
from fastapi.exceptions import HTTPException
from models.quizModels import QuizGenerationModel,QuizResultModel,ModifyQuizRequest,DiscussionWithBotBody
from utils.JsonParser import extract_json
import google.generativeai as genai
import os
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

async def getChat(history:list=None):
    if not history:
        chat = model.start_chat(history=[])
        return chat
    chat = model.start_chat(history=history)
    return chat

router=APIRouter(tags=["Quiz-Ops"])



@router.post("/discuss")
async def test(request:Request,body:DiscussionWithBotBody):
    try:
        history=await getHistory(body.quizID,request.state.user)
    except Exception:
        return JSONResponse(content="Create a quiz first",status_code=200)
    else:
        chat=await getChat(history)
        response=chat.send_message(body.text)
        return response.text


@router.post("/generateQuiz")
async def createQuiz(request:Request,body:QuizGenerationModel,db:Session=Depends(get_db)):
    try:
        chat=await getChat()
        model_instance=QuizResultModel(questionNumber=1,question= "Which of the following is NOT a primitive data type in Solidity?",options= {
                "a": "uint256",
                "b": "string",
                "c": "address",
                "d": "enum"
            }
            ,correctOption="b")
        format=model_instance.model_dump_json()
        prompt=f"Create an quiz with {body.no_of_questions} questions on the topic {body.topic} {"\n Syllabus: "+body.syllabus if body.syllabus else ""} {"\n additional preferences: "+body.preferences if body.preferences else ""}"
        prompt+=f"Return in the format {format}"
        response=chat.send_message(prompt)
        userID=request.state.user
        quiz=extract_json(response.text)
        quizID=await addQuiz(quiz)
        quiz.extend([{"quizID":quizID}])
        await addHistory(userID,quizID,[{"role": "user", "parts": prompt}, {
            "role": "model", "parts":str(response)}])
        db.add(QuizData(
            quizID=quizID,
            ownerID=request.state.user,
            topic=body.topic,
            number_of_questions=body.no_of_questions,
            syllabus=body.syllabus
        ))
        
        
    except Exception as e:
        return JSONResponse(content=str(e))
    else:
        db.commit()
        return quiz


@router.post("/modifyQuiz")
async def modifyQuiz(body:ModifyQuizRequest,request:Request,db:Session=Depends(get_db)):
    try:
        
        result=db.query(QuizData).filter_by(quizID=body.quizID).first()
        if result.ownerID!=request.state.user:
            raise HTTPException(detail="Only the owner can modify the Quiz",status_code=401)
        currentHistory=await getHistory(body.quizID,request.state.user)
        chat=await getChat(currentHistory)
        prompt=f"Make these changes:{body.changes}"
        modifiedQuizResponse=chat.send_message(prompt)
        modifiedQuiz=extract_json(modifiedQuizResponse.text)
        currentHistory.extend([{"role": "user", "parts": prompt}, {
        "role": "model", "parts":str( modifiedQuizResponse)}])     
        await modifyHistory(body.quizID,request.state.user,currentHistory)    
        return modifiedQuiz
    except Exception as e:
        return JSONResponse(content=str(e))
    

@router.get("/getQuiz")
async def retrieveQuiz(quizID:str=Query(...)):
    return JSONResponse(content=await getQuiz(quizID))




        

    
