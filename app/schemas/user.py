
from pydantic import BaseModel
from typing import Optional

class UserProfileUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str]= None
    email: Optional[str] = None