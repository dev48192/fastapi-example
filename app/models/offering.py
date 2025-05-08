from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base

class Offering(Base):
    __tablename__ = "offerings"

    id = Column(Integer, primary_key=True)
    business_id = Column(ForeignKey("businesses.id"), nullable=False)
    catalog_item_id = Column(ForeignKey("catalog_items.id"), nullable=False)

    min_order_quantity = Column(Float, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    business = relationship("Business", back_populates="offerings")
    catalog_item = relationship("CatalogItem")