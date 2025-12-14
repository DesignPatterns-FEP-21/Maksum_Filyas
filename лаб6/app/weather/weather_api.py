#Цей файл робить асинхронний запит до сервісу OpenWeatherMap, 
# щоб отримати актуальну погоду (температуру та стан, наприклад "Rainy") для вказаного міста.
import httpx
from typing import Optional
from app.core.config import settings
from app.core.logger import logger
from app.db.models import Weather

class WeatherAPI:
    """Клас для інтеграції з OpenWeatherMap API."""
    
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    async def get_weather(self, city: str) -> Optional[Weather]:
        """
        Отримує поточну погоду для вказаного міста.
        [cite: 10, 18]
        """
        if not settings.OPENWEATHER_API_KEY:
            logger.error("OPENWEATHER_API_KEY не встановлено!")
            return None

        params = {
            "q": city,
            "appid": settings.OPENWEATHER_API_KEY,
            "units": "metric" # Температура в C
        }

        try:
            async with httpx.AsyncClient() as client:
                logger.info(f"Запит погоди для {city}...")
                response = await client.get(self.BASE_URL, params=params)
                response.raise_for_status() # Генерує виключення для 4xx/5xx
                
                data = response.json()
                
                # Парсимо відповідь
                condition = data["weather"][0]["main"] # Напр., "Rain", "Clouds", "Clear"
                description = data["weather"][0]["description"]
                temperature = data["main"]["temp"]
                
                logger.info(f"Погоду отримано: {city} - {condition} ({temperature}°C)")
                
                return Weather(
                    condition=condition,
                    temperature=temperature,
                    description=description
                )

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP помилка при запиті до OpenWeatherMap: {e}")
        except Exception as e:
            logger.error(f"Помилка при отриманні погоди: {e}")
        
        return None

# Єдиний екземпляр клієнта API
weather_api_client = WeatherAPI()