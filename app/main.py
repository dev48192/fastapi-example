from fastapi import FastAPI
from app.routes import example, auth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "https://ebc-app-9e775.web.app",         # Firebase default domain
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # or limit to ["GET", "POST"] for more security
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth")
app.include_router(example.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI Starter!"}
