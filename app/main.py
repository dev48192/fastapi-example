from fastapi import FastAPI, Request
from app.routes import user, auth, business, offering
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "https://ebc-app-9e775.web.app",         # Firebase default 
    "https://ebc-app-9e775.firebaseapp.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # or limit to ["GET", "POST"] for more security
    allow_headers=["*"],
)

app.include_router(auth, prefix="/api/auth")
app.include_router(user, prefix="/api")
app.include_router(business, prefix="/api")
app.include_router(offering, prefix="/api")

@app.get("/debug/cookies")
def debug_cookies(request: Request):
    # Return the cookies sent in the request
    return {"cookies": request.cookies}

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI Starter!"}
