# ПАТЕРН "СТРАТЕГІЯ" - КОНКРЕТНА СТРАТЕГІЯ
from app.core.logger import logger
from typing import List
from .base import WeatherStrategy
from app.db.models import Activity, UserPreferences

class SunnyWeatherStrategy(WeatherStrategy):
    """
    Стратегія для сонячної погоди.
    Пропонує активності на свіжому повітрі.
    """
    
    def get_activities(self, preferences: UserPreferences) -> List[Activity]:
        activities = []
        
        # 1. Прогулянка в парку (outdoor)
        if "outdoor" in preferences.preferred_types and "hiking" not in preferences.avoid_types:
            activities.append(Activity(name="Прогулянка в парку", type="outdoor", priority=1))

        # 2. Спорт на вулиці (sport)
        if "sport" not in preferences.avoid_types:
            activities.append(Activity(name="Спорт на вулиці", type="sport", priority=2))
            
        # 3. Читання книги на балконі (relax)
        activities.append(Activity(name="Читання на балконі", type="relax", priority=3))
        
        logger.info(f"SunnyStrategy: generated {len(activities)} activities.")
        return activities