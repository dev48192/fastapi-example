from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models import User
from app.db import get_db
from app.utils import get_current_user
from app.schemas import UserProfileUpdate

router = APIRouter()

@router.put("/profile")
async def update_profile(
    payload: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(current_user, field, value)

    db.commit()
    db.refresh(current_user)

    return {"message": "Profile updated", "user": {
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "email": current_user.email,
        "is_seller": current_user.is_seller
    }}

