# app/models/permiso.py
from dataclasses import dataclass

@dataclass
class Permiso:
    nombre: str
    descripcion: str = ""
