import pytest
from pydantic import ValidationError
from app.db.models import UserPreferences, Weather, WorkingHours

@pytest.fixture
def mock_user_preferences():
    """Фікстура (зразок) для вподобань користувача."""
    return UserPreferences(
        user_id="test_user",
        preferred_types=["outdoor", "learning"],
        avoid_types=["sport"],
        working_hours=WorkingHours(start=9, end=17)
    )

def test_model_user_preferences_creation(mock_user_preferences):
    """Тест 1: Успішне створення моделі UserPreferences."""
    assert mock_user_preferences.user_id == "test_user"
    assert "outdoor" in mock_user_preferences.preferred_types
    assert mock_user_preferences.working_hours.start == 9

def test_model_validation_error():
    """Тест 2: Pydantic має 'впасти' при некоректних даних (година 25)."""
    with pytest.raises(ValidationError):
        # 'start' не може бути 25
        WorkingHours(start=25, end=17)