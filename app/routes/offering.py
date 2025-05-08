from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Business, Offering, CatalogItem, Brand, OfferingBrand
from app.schemas.offering import OfferingsBatchCreate, OfferingUpdateRequest
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

    created_count = 0
    for item in payload.offerings:
        catalog_item = db.query(CatalogItem).filter_by(id=item.catalog_item_id).first()
        if not catalog_item:
            raise HTTPException(status_code=404, detail=f"Catalog item {item.catalog_item_id} not found")

        # Create the offering
        offering = Offering(
            business_id=business.id,
            catalog_item_id=item.catalog_item_id,
            min_order_quantity=item.min_order_quantity
        )
        db.add(offering)
        db.flush()  # Get offering.id before committing

        # Add associated brands
        for brand_id in item.brand_ids:
            brand = db.query(Brand).filter_by(id=brand_id).first()
            if not brand:
                raise HTTPException(status_code=404, detail=f"Brand {brand_id} not found")

            db.add(OfferingBrand(offering_id=offering.id, brand_id=brand_id))

        created_count += 1

    db.commit()

    return {"message": f"{created_count} offerings created successfully."}

@router.get("/offerings")
def get_offerings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    business = db.query(Business).filter(Business.user_id == current_user.id).first()
    if not business:
        raise HTTPException(status_code=400, detail="Business not found for user")

    offerings = db.query(Offering).filter(Offering.business_id == business.id).all()

    result = []
    for offering in offerings:
        item_name = offering.catalog_item.name if offering.catalog_item else None
        brand_names = [brand.name for brand in offering.brands]

        result.append({
            "offering_id": offering.id,
            "catalog_item_id": offering.catalog_item_id,
            "catalog_item_name": item_name,
            "min_order_quantity": offering.min_order_quantity,
            "brand_names": brand_names,
        })

    return {"offerings": result}


@router.put("/offerings/{offering_id}")
def update_offering(
    offering_id: int,
    payload: OfferingUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    offering = db.query(Offering).join(Business).filter(
        Offering.id == offering_id,
        Business.user_id == current_user.id
    ).first()

    if not offering:
        raise HTTPException(status_code=404, detail="Offering not found")

    if payload.min_order_quantity is not None:
        offering.min_order_quantity = payload.min_order_quantity

    if payload.brand_ids is not None:
        # Remove old brands
        db.query(OfferingBrand).filter_by(offering_id=offering.id).delete()
        # Add new brands
        for brand_id in payload.brand_ids:
            db.add(OfferingBrand(offering_id=offering.id, brand_id=brand_id))

    db.commit()
    db.refresh(offering)

    return {"message": "Offering updated successfully"}

@router.delete("/offerings/{offering_id}")
def delete_offering(
    offering_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    offering = db.query(Offering).join(Business).filter(
        Offering.id == offering_id,
        Business.user_id == current_user.id
    ).first()

    if not offering:
        raise HTTPException(status_code=404, detail="Offering not found")

    # Delete associated brand links
    db.query(OfferingBrand).filter_by(offering_id=offering.id).delete()

    db.delete(offering)
    db.commit()

    return {"message": "Offering deleted successfully"}
