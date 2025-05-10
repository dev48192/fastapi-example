from fastapi import APIRouter, Response, Request, Cookie, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.firebase_config import firebase_auth
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

        # Set cookie for 5 days (can adjust based on your need)
        expires = datetime.utcnow() + timedelta(days=5)
        response.set_cookie(
            key="session",
            value=payload.id_token,
            httponly=True,
            secure=True,  # Set to False for local dev if needed
            samesite="Lax",
            expires=expires.strftime("%a, %d-%b-%Y %H:%M:%S GMT"),
        )

        return {"message": message, "uid": uid, "phone": phone}
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid ID token: {e}")

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("session")
    return {"message": "Logged out successfully"}

@router.get("/profile")
async def profile(request: Request, db: Session = Depends(get_db)):
    id_token = request.cookies.get("session")
    if not id_token:
        raise HTTPException(status_code=401, detail="No session cookie found")

    try:
        decoded = firebase_auth.verify_id_token(id_token)
        uid = decoded["uid"]
        
        # Fetch user from database using UID
        user = db.query(User).filter(User.firebase_uid == uid).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found in database")

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

    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid session: {e}")

