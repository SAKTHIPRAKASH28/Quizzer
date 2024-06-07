import firebase_admin
from firebase_admin import credentials, auth
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from fastapi.requests import Request

cred = credentials.Certificate("quizzer-ad5cc-firebase-adminsdk-n9ngl-cd4ba46776.json")
firebase_admin.initialize_app(cred)

class FirebaseAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in {"/docs", "/openapi.json"}:
            response = await call_next(request)
            return response

        auth_header = request.headers.get("Authorization")

        if auth_header and auth_header.startswith("Bearer "):
            id_token = auth_header.split(" ")[1]
            try:
                decoded_token = auth.verify_id_token(id_token)
                request.state.user = decoded_token['user_id']
            except Exception as e:
                return JSONResponse(status_code=401, content={"detail": "Invalid token"})
        else:
            return JSONResponse(status_code=401, content={"detail": "Authorization header missing or invalid"})

        response = await call_next(request)
        return response
