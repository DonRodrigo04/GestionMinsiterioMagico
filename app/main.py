# app/main.py
import logging

from fastapi import FastAPI

from app.api.v1.spells import router as spells_router
from app.infrastructure.db import Base, engine


def configure_logging() -> None:
    """
    Configuración básica de logging.
    Si más adelante tienes logging_config.py, puedes llamar ahí.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    )


def create_app() -> FastAPI:
    """
    Crea y configura la aplicación FastAPI.
    """
    configure_logging()

    app = FastAPI(
        title="Ministerio de Magia API",
        version="0.1.0",
    )

    # Crear tablas en la base de datos (no hace nada si no hay modelos ORM)
    Base.metadata.create_all(bind=engine)

    # Incluir routers
    app.include_router(spells_router)

    # Endpoint sencillo de healthcheck
    @app.get("/health", tags=["system"])
    async def health():
        return {"status": "ok"}

    return app


# Instancia que usará Uvicorn / Gunicorn
app = create_app()


if __name__ == "__main__":
    import uvicorn

    # Ejecutar con: python -m app.main
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )

