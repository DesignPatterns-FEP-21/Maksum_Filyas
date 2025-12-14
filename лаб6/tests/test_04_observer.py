# tests/test_04_observer.py
import pytest
from unittest.mock import Mock, patch
from app.weather.weather_station import WeatherStation, IWeatherObserver
from app.db.models import Weather

@pytest.fixture
def weather_station():
    """Створює чисту 'WeatherStation' для кожного тесту."""
    station = WeatherStation()
    # Очищуємо спостерігачів, бо 'weather_station' в коді - це сінглтон
    station._observers = [] 
    station._current_weather = None
    return station

@pytest.fixture
def mock_observer():
    """Створює мок-об'єкт (імітацію) спостерігача."""
    # Mock(spec=...) створює об'єкт, який має ті ж методи, що й інтерфейс
    observer = Mock(spec=IWeatherObserver)
    return observer

def test_observer_attach(weather_station, mock_observer):
    """Тест 9 (Спостерігач): Спостерігач успішно додається до списку."""
    assert len(weather_station._observers) == 0
    weather_station.attach(mock_observer)
    assert len(weather_station._observers) == 1
    assert weather_station._observers[0] == mock_observer

@pytest.mark.asyncio
# 'patch' імітує 'weather_api_client.get_weather', щоб не робити реальний запит
@patch('app.weather.weather_api.weather_api_client.get_weather')
async def test_observer_notify_only_on_change(mock_get_weather, weather_station, mock_observer):
    """Тест 10 (Спостерігач): 'update' викликається лише при зміні умови погоди."""
    
    # 1. Прикріплюємо спостерігача
    weather_station.attach(mock_observer)
    
    # 2. Мокаємо першу відповідь API (Дощ)
    weather_1_rain = Weather(condition="Rain", temperature=10.0)
    mock_get_weather.return_value = weather_1_rain
    
    # 3. Запускаємо перевірку
    await weather_station.fetch_weather("Lviv")
    
    # 4. Перевіряємо: 'update' було викликано 1 раз
    mock_observer.update.assert_called_once_with(weather_1_rain, "Lviv")
    
    # 5. Мокаємо другу відповідь API (Знову Дощ)
    weather_2_rain_again = Weather(condition="Rain", temperature=11.0) # Умова та сама!
    mock_get_weather.return_value = weather_2_rain_again
    
    # 6. Запускаємо перевірку
    await weather_station.fetch_weather("Lviv")
    
    # 7. Перевіряємо: 'update' НЕ було викликано знову. Загальна к-сть викликів = 1
    mock_observer.update.assert_called_once() 

    # 8. Мокаємо третю відповідь API (Сонце)
    weather_3_sun = Weather(condition="Sun", temperature=15.0) # Умова ЗМІНИЛАСЬ
    mock_get_weather.return_value = weather_3_sun

    # 9. Запускаємо перевірку
    await weather_station.fetch_weather("Lviv")
    
    # 10. Перевіряємо: 'update' було викликано вдруге
    assert mock_observer.update.call_count == 2
    mock_observer.update.assert_called_with(weather_3_sun, "Lviv") # Перевірка останнього виклику