from pydantic import BaseModel
from typing import Optional
from enum import Enum

class BusinessTypeEnum(str, Enum):
    retailer = "Retailer"
    wholesaler = "Wholesaler"
    manufacturer = "Manufacturer"

class BusinessUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    gstin: Optional[str] = None
    business_type: Optional[BusinessTypeEnum] = None
