# app/services/metrics_service.py
from collections import defaultdict
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class MetricsService:
    """
    Servicio simple de métricas.
    En un entorno real podrías integrar con Prometheus.
    """

    def __init__(self):
        # Historial de latencias por nombre de métrica
        self.latency_histogram: Dict[str, List[float]] = defaultdict(list)

    def registrar_tiempo_respuesta(self, metric_name: str, elapsed: float) -> None:
        self.latency_histogram[metric_name].append(elapsed)
        logger.debug("METRIC | %s | latency=%f", metric_name, elapsed)
