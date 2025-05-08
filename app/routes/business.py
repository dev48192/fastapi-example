from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Business, User
from app.db import get_db
from app.utils import get_current_user
from app.schemas.business import BusinessUpdate

router = APIRouter()

@router.put("/business")
async def update_or_create_business(
    payload: BusinessUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    business = db.query(Business).filter(Business.user_id == current_user.id).first()

    if business:
        for field, value in payload.dict(exclude_unset=True).items():
            setattr(business, field, value)
        message = "Business updated successfully."
    else:
        business = Business(user_id=current_user.id, **payload.dict(exclude_unset=True))
        db.add(business)
        message = "Business created successfully."

    db.commit()
    db.refresh(business)

    return {"message": message, "business": {
        "id": business.id,
        "name": business.name,
        "address": business.address,
        "gst_number": business.gst_number,
        "business_type": business.business_type
    }}
