# app/schemas/hechizo.py
from pydantic import BaseModel
from typing import Optional

class HechizoBase(BaseModel):
    nombre: str
    tipo: Optional[str] = None
    nivel_peligro: int = 1

class HechizoCreate(HechizoBase):
    pass

class HechizoRead(HechizoBase):
    id: int

    class Config:
        orm_mode = True
