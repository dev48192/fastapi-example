
from pydantic import BaseModel
from typing import Optional

class UserProfileUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]