from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base
import enum

class CatalogTypeEnum(str, enum.Enum):
    Material = "Material"
    Service = "Service"


class CatalogItem(Base):
    __tablename__ = "catalog_items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    type = Column(Enum(CatalogTypeEnum), nullable=False)    
    description = Column(String, nullable=True)
    unit = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    brands = relationship("Brand", secondary="catalog_item_brands", back_populates="catalog_items")