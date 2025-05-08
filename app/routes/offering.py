from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Business, Offering, CatalogItem
from app.schemas.offering import OfferingsBatchCreate
from app.utils import get_current_user
from app.models import User

router = APIRouter()

@router.post("/offerings")
def create_offerings(
    payload: OfferingsBatchCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    business = db.query(Business).filter(Business.user_id == current_user.id).first()
    if not business:
        raise HTTPException(status_code=400, detail="Business not found for user")

    offerings_to_create = []
    for item in payload.offerings:
        # Optional: Check if catalog item exists
        catalog_exists = db.query(CatalogItem).filter_by(id=item.catalog_item_id).first()
        if not catalog_exists:
            raise HTTPException(status_code=404, detail=f"Catalog item {item.catalog_item_id} not found")

        offerings_to_create.append(
            Offering(
                business_id=business.id,
                catalog_item_id=item.catalog_item_id,
                min_order_quantity=item.min_order_quantity
            )
        )

    db.add_all(offerings_to_create)
    db.commit()

    return {"message": f"{len(offerings_to_create)} offerings created successfully."}
