import pytest
from app.db.models import UserPreferences
from app.planner.strategies.sunny import SunnyWeatherStrategy
from app.planner.strategies.rainy import RainyWeatherStrategy

@pytest.fixture
def prefs_love_outdoor_hate_sport():
    """Вподобання: Любить вулицю, ненавидить спорт."""
    return UserPreferences(user_id="u1", preferred_types=["outdoor"], avoid_types=["sport"])

@pytest.fixture
def prefs_love_indoor_hate_learning():
    """Вподобання: Любить вдома, ненавидить вчитися."""
    return UserPreferences(user_id="u2", preferred_types=["indoor", "productive"], avoid_types=["learning"])


def test_strategy_sunny_prefers_outdoor(prefs_love_outdoor_hate_sport):
    """Тест 3 (Стратегія): Сонячна стратегія пропонує 'Прогулянка в парку', 
    бо 'outdoor' є в preferred_types."""
    strategy = SunnyWeatherStrategy()
    activities = strategy.get_activities(prefs_love_outdoor_hate_sport)
    activity_names = [a.name for a in activities]
    assert "Прогулянка в парку" in activity_names

def test_strategy_sunny_avoids_sport(prefs_love_outdoor_hate_sport):
    """Тест 4 (Стратегія): Сонячна стратегія НЕ пропонує 'Спорт', 
    бо 'sport' є в avoid_types."""
    strategy = SunnyWeatherStrategy()
    activities = strategy.get_activities(prefs_love_outdoor_hate_sport)
    activity_names = [a.name for a in activities]
    assert "Спорт на вулиці" not in activity_names

def test_strategy_rainy_prefers_indoor(prefs_love_indoor_hate_learning):
    """Тест 5 (Стратегія): Дощова стратегія пропонує 'Робота по дому', 
    бо 'indoor' є в preferred_types."""
    strategy = RainyWeatherStrategy()
    activities = strategy.get_activities(prefs_love_indoor_hate_learning)
    activity_names = [a.name for a in activities]
    assert "Робота по дому" in activity_names

def test_strategy_rainy_avoids_learning(prefs_love_indoor_hate_learning):
    """Тест 6 (Стратегія): Дощова стратегія НЕ пропонує 'Навчання', 
    бо 'learning' є в avoid_types."""
    strategy = RainyWeatherStrategy()
    activities = strategy.get_activities(prefs_love_indoor_hate_learning)
    activity_names = [a.name for a in activities]
    assert "Навчання (онлайн-курс)" not in activity_names