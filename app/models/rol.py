# app/models/rol.py
from dataclasses import dataclass, field
from typing import List

from .permiso import Permiso

@dataclass
class Rol:
    nombre: str
    permisos: List[Permiso] = field(default_factory=list)
