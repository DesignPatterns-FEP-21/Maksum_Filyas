# tests/test_03_weather_api.py
import pytest
import respx
from httpx import Response
from app.weather.weather_api import weather_api_client
from app.core.config import settings

# Встановлюємо фейковий ключ для тестів
settings.OPENWEATHER_API_KEY = "test_key_for_pytest"

@pytest.mark.asyncio
@respx.mock
async def test_weather_api_get_weather_success():
    """Тест 7 (API): Успішне отримання та парсинг погоди (мок)."""
    
    # Імітуємо відповідь від OpenWeatherMap
    mock_response = {
        "weather": [{"main": "Clouds", "description": "few clouds"}],
        "main": {"temp": 15.0}
    }
    # Кажемо 'respx' перехопити запит і повернути наш mock_response
    respx.get(weather_api_client.BASE_URL).mock(return_value=Response(200, json=mock_response))
    
    weather = await weather_api_client.get_weather("Lviv")
    
    assert weather is not None
    assert weather.condition == "Clouds"
    assert weather.temperature == 15.0
    assert weather.description == "few clouds"

@pytest.mark.asyncio
@respx.mock
async def test_weather_api_get_weather_fail_404():
    """Тест 8 (API): API повертає None у разі помилки 404 (місто не знайдено)."""
    
    # Імітуємо відповідь 404
    respx.get(weather_api_client.BASE_URL).mock(return_value=Response(404))
    
    weather = await weather_api_client.get_weather("NonExistentCity")
    
    assert weather is None