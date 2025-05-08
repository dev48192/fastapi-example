from sqlalchemy import Column, Integer, ForeignKey, Table
from app.db import Base

class CatalogItemBrand(Base):
    __tablename__ = "catalog_item_brands"

    id = Column(Integer, primary_key=True)
    catalog_item_id = Column(Integer, ForeignKey("catalog_items.id"), nullable=False)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False)