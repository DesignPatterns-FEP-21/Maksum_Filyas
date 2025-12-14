# ПАТЕРН "СПОСТЕРІГАЧ" (OBSERVER) - СУБ'ЄКТ (SUBJECT/OBSERVABLE)
#Це "погодна станція" (патерн "Суб'єкт") [cite: 47]: вона перевіряє погоду, 
# і якщо вона змінилася, то сповіщає всі підписані на неї модулі (наприклад, DayPlanner), 
# що їм потрібно оновити свої дані.
from __future__ import annotations
from typing import List, Optional
from app.db.models import Weather
from app.core.logger import logger
from .weather_api import weather_api_client

# Інтерфейс Спостерігача (Observer)
class IWeatherObserver:
    """Інтерфейс для об'єктів, що реагують на зміну погоди."""
    def update(self, weather: Weather, city: str):
        raise NotImplementedError

class WeatherStation:
    """
    Суб'єкт (Observable).
    Він відстежує погоду і сповіщає спостерігачів про зміни. [cite: 47]
    """
    
    _observers: List[IWeatherObserver] = []
    _current_weather: Optional[Weather] = None
    _current_city: str = ""

    def attach(self, observer: IWeatherObserver) -> None:
        """Прикріплює спостерігача."""
        if observer not in self._observers:
            self._observers.append(observer)
            logger.info(f"Observer {observer.__class__.__name__} attached.")

    def detach(self, observer: IWeatherObserver) -> None:
        """Відкріплює спостерігача."""
        if observer in self._observers:
            self._observers.remove(observer)
            logger.info(f"Observer {observer.__class__.__name__} detached.")

    def notify(self) -> None:
        """
        Сповіщає всіх спостерігачів про зміну стану. [cite: 49]
        """
        logger.info(f"Notifying {len(self._observers)} observers...")
        for observer in self._observers:
            observer.update(self._current_weather, self._current_city)

    async def fetch_weather(self, city: str) -> None:
        """
        Отримує погоду з API та сповіщає спостерігачів, 
        ЯКЩО погода змінилася. [cite: 48]
        """
        logger.info(f"WeatherStation: fetching weather for {city}...")
        new_weather = await weather_api_client.get_weather(city)
        
        if new_weather is None:
            logger.warning("Weather fetch failed. No update.")
            return

        # Сповіщаємо, лише якщо стан змінився
        # (зміна міста АБО зміна погодних умов)
        if (self._current_weather is None or 
            self._current_weather.condition != new_weather.condition or
            self._current_city != city):
            
            logger.info(f"Weather changed! New: {new_weather.condition}. Old: {self._current_weather.condition if self._current_weather else 'N/A'}")
            
            self._current_weather = new_weather
            self._current_city = city
            self.notify() # [cite: 49]
        else:
            logger.info("Weather condition unchanged. No notification.")

# Єдиний екземпляр станції
weather_station = WeatherStation()