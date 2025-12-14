# ПАТЕРН "СТРАТЕГІЯ" - КОНКРЕТНА СТРАТЕГІЯ
from typing import List
from .base import WeatherStrategy
from app.db.models import Activity, UserPreferences
from app.core.logger import logger

class CloudyWeatherStrategy(WeatherStrategy):
    """
    Стратегія для хмарної погоди. 
    Пропонує нейтральні активності, які можна робити як вдома, так і на вулиці.
    """
    
    def get_activities(self, preferences: UserPreferences) -> List[Activity]:
        activities = []
        
        # 1. Відвідати музей або кафе (indoor/social)
        if "social" not in preferences.avoid_types:
            activities.append(Activity(name="Відвідати музей або кафе", type="indoor", priority=2))

        # 2. Читання книги (relax/learning)
        if "learning" in preferences.preferred_types or "relax" in preferences.preferred_types:
            activities.append(Activity(name="Читання книги", type="relax", priority=1))
            
        # 3. Легка прогулянка (outdoor)
        if "outdoor" in preferences.preferred_types and "outdoor" not in preferences.avoid_types:
            activities.append(Activity(name="Коротка прогулянка", type="outdoor", priority=3))
        
        logger.info(f"CloudyStrategy: generated {len(activities)} activities.")
        return activities