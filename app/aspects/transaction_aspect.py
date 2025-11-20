# app/aspects/transaction_aspect.py
import inspect
from functools import wraps
from typing import Optional

from sqlalchemy.orm import Session


def transactional(db_arg_name: str = "db"):
    """
    Aspecto de transacción:
    Usa la sesión SQLAlchemy recibida como parámetro (por defecto 'db').
    Hace commit si todo va bien, rollback si hay excepción.
    """
    def decorator(target):
        is_async = inspect.iscoroutinefunction(target)

        @wraps(target)
        async def async_wrapper(*args, **kwargs):
            db: Optional[Session] = kwargs.get(db_arg_name)
            if db is None:
                return await target(*args, **kwargs)

            try:
                result = await target(*args, **kwargs)
                db.commit()
                return result
            except Exception:
                db.rollback()
                raise

        @wraps(target)
        def sync_wrapper(*args, **kwargs):
            db: Optional[Session] = kwargs.get(db_arg_name)
            if db is None:
                return target(*args, **kwargs)

            try:
                result = target(*args, **kwargs)
                db.commit()
                return result
            except Exception:
                db.rollback()
                raise

        return async_wrapper if is_async else sync_wrapper

    return decorator
