from firebase_admin import firestore
from fastapi import HTTPException


dbClient=firestore.client()
db=dbClient.collection('histories')


async def addHistory(userID:str,quizID:str,history:list[dict])->None:
    doc=db.document(userID)
    doc.set({quizID:history})

async def getHistory(quizID:str,userID:str)->list[dict]:
    doc_ref = db.document(userID)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()[quizID]
    else:
        raise HTTPException(detail="history not found",status_code=404)
    
async def modifyHistory(quizID:str,userID:str,history:list[dict])->None:
    db.document(userID).update({quizID:history})
