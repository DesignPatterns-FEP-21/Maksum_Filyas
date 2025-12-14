import time
from typing import List, Dict, Any
from drones.utils.logger import setup_logger

logger = setup_logger("Telemetry")

class TelemetryService:
    """
    Сервіс для запису метрик під час польоту (швидкість, висота, заряд батареї).
    Дозволяє зберігати історію змін параметрів дрона.
    """
    def __init__(self):
        self._metrics: List[Dict[str, Any]] = []

    def record(self, metric_name: str, value: Any):
        """Записує показник з часовою міткою."""
        entry = {
            "timestamp": time.time(),
            "metric": metric_name,
            "value": value
        }
        self._metrics.append(entry)

    def get_report(self) -> List[Dict[str, Any]]:
        """Повертає всю зібрану телеметрію."""
        return self._metrics