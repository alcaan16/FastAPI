from pydantic import BaseModel
from typing import Optional

class Usuario(BaseModel):
    id: Optional[str] = None
    username: str
    email: str