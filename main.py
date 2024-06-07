from fastapi import FastAPI
from middlewares.authmiddleware import FirebaseAuthMiddleware
from fastapi.requests import Request
from src import quizBot
import uvicorn
import os


app=FastAPI(title="Quizzer")
app.add_middleware(FirebaseAuthMiddleware)
app.include_router(quizBot.router)

@app.get("/helloworld")
async def protected_route(request: Request):
    user = request.state.user
    return {"message": f"Hello {user['email']}, you are authenticated"}


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)