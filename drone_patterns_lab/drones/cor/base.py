from abc import ABC, abstractmethod
from typing import Optional

class Handler(ABC):
    """
    Абстрактний базовий клас обробника (Chain of Responsibility).
    Визначає інтерфейс для обробки запитів та посилання на наступного обробника.
    """
    def __init__(self, next_handler: Optional['Handler'] = None):
        self._next_handler = next_handler

    def set_next(self, handler: 'Handler') -> 'Handler':
        """Встановлює наступного обробника у ланцюжку."""
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, issue: str, context) -> bool:
        """
        Метод обробки.
        issue: Опис проблеми
        context: Об'єкт місії, щоб мати доступ до контролера дрона.
        return: True, якщо проблему вирішено, інакше передає далі.
        """
        if self._next_handler:
            return self._next_handler.handle(issue, context)
        return False