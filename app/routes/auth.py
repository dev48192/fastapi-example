from fastapi import APIRouter, Response, Request, Cookie, HTTPException
from pydantic import BaseModel
from app.firebase_config import firebase_auth
from datetime import datetime, timedelta


router = APIRouter()

class OTPLoginRequest(BaseModel):
    id_token: str


@router.post("/login")
async def login(payload: OTPLoginRequest, response: Response):
    try:
        decoded = firebase_auth.verify_id_token(payload.id_token)
        uid = decoded["uid"]
        phone = decoded.get("phone_number")

        # Set cookie for 5 days
        expires = datetime.utcnow() + timedelta(days=5)
        response.set_cookie(
            key="session",
            value=payload.id_token,
            httponly=True,
            secure=True,  # Set to False for local dev if needed
            samesite="Lax",
            expires=expires.strftime("%a, %d-%b-%Y %H:%M:%S GMT"),
        )

        return {"message": "Login successful", "uid": uid, "phone": phone}
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid ID token: {e}")

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("session")
    return {"message": "Logged out successfully"}

@router.post("/profile")
async def profile(request: Request):
    id_token = request.cookies.get("session")
    if not id_token:
        raise HTTPException(status_code=401, detail="No session cookie found")

    try:
        decoded = firebase_auth.verify_id_token(id_token)
        return {"uid": decoded["uid"], "phone": decoded.get("phone_number")}
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid session: {e}")

    
      