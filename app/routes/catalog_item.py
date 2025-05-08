from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import CatalogItem, Brand, User, CatalogTypeEnum
from app.schemas.catalog import CatalogItemOut, BrandOut
from app.utils import get_current_user  # Auth util

router = APIRouter()

@router.get("/catalog-items", response_model=list[CatalogItemOut])
def get_catalog_items(
    type: CatalogTypeEnum = Query(..., description="Material or Service"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # 🔒 Authentication
):
    items = db.query(CatalogItem).filter(CatalogItem.type == type).all()
    return items


@router.get("/catalog-items/{catalog_item_id}/brands", response_model=list[BrandOut])
def get_brands_for_catalog_item(
    catalog_item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # 🔒 Authentication
):
    catalog_item = db.query(CatalogItem).filter_by(id=catalog_item_id).first()
    if not catalog_item:
        raise HTTPException(status_code=404, detail="Catalog item not found")

    return catalog_item.brands
