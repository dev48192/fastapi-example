from fastapi import APIRouter, Response, Request, Cookie, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.firebase_config import firebase_auth
from app.utils import get_current_user
from datetime import datetime, timedelta
from app.db import SessionLocal, get_db
from app.models.user import User  # Assuming you have a User model in models.py

router = APIRouter()

class OTPLoginRequest(BaseModel):
    id_token: str

@router.post("/login")
async def login(payload: OTPLoginRequest, response: Response, db: Session = Depends(get_db)):
    try:
        # Verify Firebase ID token
        decoded = firebase_auth.verify_id_token(payload.id_token)
        uid = decoded["uid"]
        phone = decoded.get("phone_number")

        # Check if the user exists in the database
        user = db.query(User).filter(User.firebase_uid == uid).first()
        
        if not user:
            # Create a new user if not exists
            new_user = User(firebase_uid=uid, phone_number=phone)
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            message = "Registration successful, welcome aboard!"
        else:
            message = "Login successful, welcome back!"
            
        return {
            "message": message,
            "user":  {
                "uid": user.firebase_uid,
                "phone": user.phone_number,
                "created_at": user.created_at, 
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "is_seller": user.is_seller
            }
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid ID token: {e}")

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("session")
    return {"message": "Logged out successfully"}

@router.get("/profile")
async def profile(user: User = Depends(get_current_user)):
    # Return user info (sanitize sensitive fields as needed)
    return {
        "uid": user.firebase_uid,
        "phone": user.phone_number,
        "created_at": user.created_at,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "is_seller": user.is_seller
    }