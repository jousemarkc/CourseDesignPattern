from pydantic import BaseModel
from typing import Optional

class ContactInfo(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None