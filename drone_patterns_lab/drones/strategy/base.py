from abc import ABC, abstractmethod
from typing import Dict, Any

class ReactionStrategy(ABC):
    """
    Абстрактна стратегія. Не можна створювати екземпляри цього класу!
    [cite_start][cite: 100-101]
    """
    @abstractmethod
    def react(self, mission_context, reading: Dict[str, Any]):
        pass

# --- ВАЖЛИВО: ЦЕЙ КЛАС МАЄ БУТИ ТУТ ---
class NoReaction(ReactionStrategy):
    """
    Стратегія "за замовчуванням" (Null Object).
    Використовується, коли для середовища немає специфічної реакції.
    Вона МАЄ реалізовувати метод react, навіть якщо він порожній.
    """
    def react(self, mission_context, reading: Dict[str, Any]):
        # Метод реалізований (щоб клас не був абстрактним), але нічого не робить
        pass