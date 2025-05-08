from pydantic import BaseModel
from app.models import CatalogTypeEnum

class CatalogItemOut(BaseModel):
    id: int
    name: str
    unit: str | None
    description: str | None
    type: CatalogTypeEnum

    class Config:
        orm_mode = True


class BrandOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
