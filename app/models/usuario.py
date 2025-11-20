# app/models/usuario.py
from dataclasses import dataclass, field
from typing import List

from .rol import Rol
from .permiso import Permiso

@dataclass
class Usuario:
    id: int
    nombre: str
    roles: List[Rol] = field(default_factory=list)

    def has_permissions(self, perm_names: List[str]) -> bool:
        """
        Comprueba si el usuario tiene TODOS los permisos indicados por nombre.
        """
        user_perms = {p.nombre for r in self.roles for p in r.permisos}
        return all(p in user_perms for p in perm_names)
