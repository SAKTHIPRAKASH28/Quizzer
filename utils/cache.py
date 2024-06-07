from cachetools import TTLCache
from fastapi.exceptions import HTTPException

'''
TTL Cache that stores the model history of specific User
Key:User Id provided by firebase Authentication
Value:History stored in the format mentioned in gemini docs
Time to live: 24hrs

'''

historyCache=TTLCache(ttl=86400,maxsize=100)

async def getHistory(userID:str)->list[dict]:
    if userID not in historyCache:
        raise HTTPException(detail="No records found",status_code=404)
    
    return historyCache[userID]

async def setUserHistory(userID:str,history:list[dict])->None:
    historyCache[userID]=history


# The following functions are deprecated.
# Developers: Please note that these functions are no longer in use
# and will be removed in future versions of this codebase.

'''
TTL Cache that stores the actual quiz
    Key:QuizID
    Value:Quiz in a List[dict] format
    Time to live: 24 hrs

'''


quizDataCache=TTLCache(ttl=86400,maxsize=100)

async def getQuiz(quizID:str)->dict:
    if quizID not in quizDataCache:
        raise HTTPException(detail="Quiz is either expired or invalid quiz ID was given",status_code=404)
    
    return quizDataCache[quizID]

async def setQuizData(quizID:str,quiz:dict)->None:
    quizDataCache[quizID]=quiz




'''
TTL Cache that maps quizID to userID
key:quizID
value:UserID
Time to live 24 hrs

'''
uidMapping=TTLCache(ttl=86400,maxsize=100)

async def getOwner(quizID:str)->str:
    if quizID not in uidMapping:
        raise HTTPException(detail="Quiz not found",status_code=404)
    return uidMapping[quizID]

async def mapOwner(quizID:str,userID:str)->None:
    uidMapping[quizID]=userID