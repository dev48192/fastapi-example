from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Business
from app.schemas.business import BusinessUpdate
from app.utils import get_current_user
from app.models import User

router = APIRouter()

@router.put("/business")
async def update_business(
    payload: BusinessUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    business = db.query(Business).filter(Business.user_id == current_user.id).first()

    if not business:
        raise HTTPException(status_code=404, detail="Business not found")

    for field, value in payload.dict(exclude_unset=True).items():
        setattr(business, field, value)

    db.commit()
    db.refresh(business)

    return {"message": "Business updated", "business": {
        "name": business.name,
        "address": business.address,
        "gstin": business.gstin,
        "business_type": business.business_type
    }}
