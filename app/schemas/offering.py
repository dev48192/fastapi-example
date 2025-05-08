from pydantic import BaseModel
from typing import List, Optional

class OfferingItem(BaseModel):
    catalog_item_id: int
    min_order_quantity: Optional[float] = None
    brand_ids: List[int]

class OfferingsBatchCreate(BaseModel):
    offerings: List[OfferingItem]


class OfferingUpdateRequest(BaseModel):
    min_order_quantity: Optional[float] = None
    brand_ids: Optional[List[int]] = None