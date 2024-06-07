from fastapi import FastAPI
from middlewares.authmiddleware import FirebaseAuthMiddleware
from fastapi.requests import Request
from src import quizBot


app=FastAPI(title="Quizzer")
app.add_middleware(FirebaseAuthMiddleware)
app.include_router(quizBot.router)

@app.get("/helloworld")
async def protected_route(request: Request):
    user = request.state.user
    return {"message": f"Hello {user['email']}, you are authenticated"}