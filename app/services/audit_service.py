# app/services/audit_service.py
from typing import Any, Dict, Optional
import logging

from app.models.usuario import Usuario

logger = logging.getLogger(__name__)

class AuditService:
    """
    Servicio responsable de registrar eventos mágicos (auditoría).
    En un proyecto real, escribiría en una tabla de DB o fichero.
    """

    async def registrar_evento(
        self,
        actor: Optional[Usuario],
        action: str,
        success: bool,
        extra: Dict[str, Any],
    ) -> None:
        actor_name = actor.nombre if actor else "ANONYMOUS"
        logger.info(
            "AUDIT | actor=%s | action=%s | success=%s | extra=%s",
            actor_name,
            action,
            success,
            extra,
        )
