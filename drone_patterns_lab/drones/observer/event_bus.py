from typing import Dict, List, Callable
from drones.observer.events import EnvironmentEvent
from drones.utils.logger import setup_logger

logger = setup_logger("EventBus")

class EventBus:
    """
    (Observer Pattern).
    Центральний обєкт, який дозволяє компонентам підписуватися на події та публікувати їх,
    забезпечуючи слабку зв'язаність системи.
    """
    def __init__(self):
        # Словник: ключ - назва події, значення - список функцій-слухачів
        self.subscribers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, callback: Callable):
        """Реєструє функцію (callback), яка буде викликана при настанні події."""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)
        logger.debug(f"Subscribed to '{event_type}'")

    def publish(self, event: EnvironmentEvent):
        """Сповіщає всіх підписників про настання події."""
        if event.event_type in self.subscribers:
            for callback in self.subscribers[event.event_type]:
                try:
                    callback(event)
                except Exception as e:
                    logger.error(f"Error handling event {event.event_type}: {e}")