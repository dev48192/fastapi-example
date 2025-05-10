# utils/auth_utils.py

from fastapi import Request, Depends, HTTPException
from sqlalchemy.orm import Session
from app.firebase_config import firebase_auth
from app.db import get_db
from app.models import User

async def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    id_token = request.cookies.get("session")
    if not id_token:
        raise HTTPException(status_code=401, detail="No session cookie found")

    try:
        decoded = firebase_auth.verify_id_token(id_token)
        uid = decoded["uid"]
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired session")

    user = db.query(User).filter(User.firebase_uid == uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
    # return db.query(User).first()
