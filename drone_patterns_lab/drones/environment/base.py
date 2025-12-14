import random
import threading
import time
from abc import ABC, abstractmethod
from typing import Dict, Any

from drones.observer.event_bus import EventBus
from drones.observer.events import EnvironmentEvent

class Environment(ABC):
    """
    Відповідає за генерацію даних сенсорів (sample) та публікацію подій
    через  (EventBus).
    """
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.active = False

    def start(self):
        """Активує симуляцію середовища."""
        self.active = True
        # и симулюємо це при виклику sample().

    @abstractmethod
    def sample(self) -> Dict[str, Any]:
        """
        Повертає поточні показники середовища (читання сенсорів).
        """
        pass
    
    def publish_event(self, event_type: str, data: Any):
        """Допоміжний метод для публікації події."""
        event = EnvironmentEvent(event_type, data, source=self.__class__.__name__)
        self.event_bus.publish(event)