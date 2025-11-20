# app/aspects/audit_aspect.py
import inspect
from functools import wraps
from typing import Optional, Dict, Any

import anyio

from app.core.aop import _maybe_await
from app.services.audit_service import AuditService
from app.models.usuario import Usuario


def audit_log(event_type: str):
    """
    Aspecto de auditoría.
    Requiere 'audit_service' y 'current_user' en la función decorada.
    """
    def decorator(target):
        is_async = inspect.iscoroutinefunction(target)

        async def _do_audit(
            audit_service: Optional[AuditService],
            user: Optional[Usuario],
            success: bool,
            extra: Dict[str, Any],
        ):
            if not audit_service:
                return
            await _maybe_await(
                audit_service.registrar_evento,
                actor=user,
                action=event_type,
                success=success,
                extra=extra,
            )

        @wraps(target)
        async def async_wrapper(*args, **kwargs):
            audit_service: Optional[AuditService] = kwargs.get("audit_service")
            current_user: Optional[Usuario] = kwargs.get("current_user")

            extra_base = {"func": target.__name__}

            try:
                result = await target(*args, **kwargs)
                await _do_audit(audit_service, current_user, True, extra_base)
                return result
            except Exception as exc:
                extra = {**extra_base, "error": str(exc)}
                await _do_audit(audit_service, current_user, False, extra)
                raise

        @wraps(target)
        def sync_wrapper(*args, **kwargs):
            audit_service: Optional[AuditService] = kwargs.get("audit_service")
            current_user: Optional[Usuario] = kwargs.get("current_user")
            extra_base = {"func": target.__name__}

            try:
                result = target(*args, **kwargs)
                anyio.run(_do_audit, audit_service, current_user, True, extra_base)
                return result
            except Exception as exc:
                extra = {**extra_base, "error": str(exc)}
                anyio.run(_do_audit, audit_service, current_user, False, extra)
                raise

        return async_wrapper if is_async else sync_wrapper

    return decorator
