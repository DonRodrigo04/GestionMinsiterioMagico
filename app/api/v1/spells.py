# app/api/v1/spells.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.hechizo import HechizoCreate, HechizoRead
from app.api import deps
from app.models.usuario import Usuario
from app.services.spell_service import SpellService
from app.services.audit_service import AuditService
from app.aspects.security_aspect import secured
from app.aspects.audit_aspect import audit_log
from app.aspects.transaction_aspect import transactional
from app.aspects.metrics_aspect import measure_latency
from app.services.metrics_service import MetricsService

router = APIRouter(prefix="/spells", tags=["spells"])


@router.post("/cast", response_model=HechizoRead)
@secured(required_roles=["AUROR"])
@audit_log(event_type="CAST_SPELL")
@transactional()
@measure_latency(metric_name="cast_spell_latency")
async def cast_spell(
    hechizo_in: HechizoCreate,
    current_user: Usuario = Depends(deps.get_current_user),
    spell_service: SpellService = Depends(deps.get_spell_service),
    audit_service: AuditService = Depends(deps.get_audit_service),
    metrics_service: MetricsService = Depends(deps.get_metrics_service),
    db: Session = Depends(deps.get_db),
):
    """
    Lanza un hechizo.
    Seguridad, auditoría, transacción y métricas están aplicadas vía AOP.
    """
    return await spell_service.cast_spell(
        hechizo_in=hechizo_in,
        current_user=current_user,
        db=db,
    )
