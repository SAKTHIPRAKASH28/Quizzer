from firebase_admin import firestore
from fastapi import HTTPException


dbClient=firestore.client()
db=dbClient.collection('quizzes')


async def addQuiz(quiz:list[dict])->None:
    doc=db.add({"questions":quiz})
    return doc[1].id

async def getQuiz(quizID:str)->list[dict]:
    
    doc_ref = db.document(quizID)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()["questions"]
    else:
        raise HTTPException(detail="Quiz not found",status_code=404)
    
async def modifyQuiz(quizID:str,quiz:list[dict])->None:

    
    db.document(quizID).update({"questions":quiz})



    