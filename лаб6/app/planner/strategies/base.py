# ПАТЕРН "СТРАТЕГІЯ" (STRATEGY) - ІНТЕРФЕЙС СТРАТЕГІЇ
from abc import ABC, abstractmethod
from typing import List
from app.db.models import Activity, UserPreferences

class WeatherStrategy(ABC):
    """
    Інтерфейс Стратегії.
    Визначає метод, який повинні реалізувати всі конкретні стратегії. 
    """

    @abstractmethod
    def get_activities(self, preferences: UserPreferences) -> List[Activity]:
        """
        Генерує список активностей на основі погоди та вподобань. 
        """
        pass