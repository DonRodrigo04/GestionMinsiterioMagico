# app/services/spell_service.py
from sqlalchemy.orm import Session

from app.schemas.hechizo import HechizoCreate, HechizoRead
from app.models.usuario import Usuario

class SpellService:
    """
    Servicio de negocio para la gestión de hechizos.
    Aquí podrías usar repositorios, etc.
    """

    async def cast_spell(
        self,
        hechizo_in: HechizoCreate,
        current_user: Usuario,
        db: Session,
    ) -> HechizoRead:
        """
        Lanza un hechizo.
        Implementación mínima: no persiste nada, solo devuelve un objeto simulado.
        """
        # Aquí iría lógica real: validar, persistir en DB, etc.
        fake_id = 1
        return HechizoRead(id=fake_id, **hechizo_in.dict())
