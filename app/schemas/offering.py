from pydantic import BaseModel
from typing import Optional, List

class OfferingCreate(BaseModel):
    catalog_item_id: int
    min_order_quantity: Optional[float] = None

class OfferingsBatchCreate(BaseModel):
    offerings: List[OfferingCreate]
