from sqlalchemy import Column, Integer, String, Float, Enum
from app.db import Base

class CatalogItem(Base):
    __tablename__ = "catalog_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(Enum("Material", "Service", name="item_type_enum"), nullable=False)
    unit = Column(String, nullable=True)
    description = Column(String, nullable=True)