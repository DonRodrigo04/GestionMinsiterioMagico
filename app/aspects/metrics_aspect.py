# app/aspects/metrics_aspect.py
import inspect
import time
from functools import wraps

from app.services.metrics_service import MetricsService
from app.core.aop import _maybe_await


def measure_latency(metric_name: str):
    """
    Aspecto de métricas:
    Mide el tiempo de ejecución y lo envía a MetricsService.
    Requiere 'metrics_service' en los kwargs.
    """
    def decorator(target):
        is_async = inspect.iscoroutinefunction(target)

        @wraps(target)
        async def async_wrapper(*args, **kwargs):
            metrics_service: MetricsService | None = kwargs.get("metrics_service")
            start = time.perf_counter()
            try:
                return await target(*args, **kwargs)
            finally:
                elapsed = time.perf_counter() - start
                if metrics_service:
                    await _maybe_await(
                        metrics_service.registrar_tiempo_respuesta,
                        metric_name,
                        elapsed,
                    )

        @wraps(target)
        def sync_wrapper(*args, **kwargs):
            metrics_service: MetricsService | None = kwargs.get("metrics_service")
            start = time.perf_counter()
            try:
                return target(*args, **kwargs)
            finally:
                elapsed = time.perf_counter() - start
                if metrics_service:
                    metrics_service.registrar_tiempo_respuesta(metric_name, elapsed)

        return async_wrapper if is_async else sync_wrapper

    return decorator
