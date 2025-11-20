# app/api/deps.py
from typing import Generator

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.infrastructure.db import SessionLocal
from app.models.usuario import Usuario
from app.models.rol import Rol
from app.models.permiso import Permiso
from app.services.spell_service import SpellService
from app.services.audit_service import AuditService
from app.services.metrics_service import MetricsService


def get_db() -> Generator[Session, None, None]:
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user() -> Usuario:
    """
    Dependencia de ejemplo.
    En un caso real, decodificarías un JWT y buscarías el usuario en la DB.
    """
    permiso_cast = Permiso(nombre="CAST_SPELL")
    rol_auror = Rol(nombre="AUROR", permisos=[permiso_cast])
    return Usuario(id=1, nombre="Harry Potter", roles=[rol_auror])


def get_spell_service() -> SpellService:
    return SpellService()


def get_audit_service() -> AuditService:
    return AuditService()


def get_metrics_service() -> MetricsService:
    return MetricsService()
