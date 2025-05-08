from sqlalchemy import Column, Integer, ForeignKey
from app.db import Base

class OfferingBrand(Base):
    __tablename__ = "offering_brands"

    id = Column(Integer, primary_key=True)
    offering_id = Column(Integer, ForeignKey("offerings.id"), nullable=False)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False)