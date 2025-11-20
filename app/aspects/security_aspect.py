# app/aspects/security_aspect.py
import inspect
from functools import wraps
from typing import Iterable, List, Optional

from fastapi import HTTPException, status

from app.models.usuario import Usuario  # o el path que uses

def _has_any_role(user: Usuario, required_roles: Iterable[str]) -> bool:
    if not required_roles:
        return True
    user_roles = {r.nombre for r in user.roles}  # adapta a tu modelo
    return any(r in user_roles for r in required_roles)


def _has_permissions(user: Usuario, required_permissions: Iterable[str]) -> bool:
    if not required_permissions:
        return True
    # asumiendo método de dominio:
    return user.has_permissions(required_permissions)


def secured(
    required_roles: Optional[List[str]] = None,
    required_permissions: Optional[List[str]] = None,
):
    """
    Aspecto de seguridad basado en rol/permisos.
    - Requiere que la función tenga un parámetro 'current_user' (FastAPI lo injecta).
    - Se puede usar tanto en endpoints como en servicios si se pasa current_user.
    """
    required_roles = required_roles or []
    required_permissions = required_permissions or []

    def decorator(target):
        is_async = inspect.iscoroutinefunction(target)

        @wraps(target)
        async def async_wrapper(*args, **kwargs):
            current_user: Usuario = kwargs.get("current_user")
            if current_user is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Usuario no autenticado",
                )

            if not _has_any_role(current_user, required_roles):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Rol insuficiente",
                )

            if not _has_permissions(current_user, required_permissions):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Permisos insuficientes",
                )

            return await target(*args, **kwargs)

        @wraps(target)
        def sync_wrapper(*args, **kwargs):
            current_user: Usuario = kwargs.get("current_user")
            if current_user is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Usuario no autenticado",
                )

            if not _has_any_role(current_user, required_roles):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Rol insuficiente",
                )

            if not _has_permissions(current_user, required_permissions):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Permisos insuficientes",
                )

            return target(*args, **kwargs)

        return async_wrapper if is_async else sync_wrapper

    return decorator
