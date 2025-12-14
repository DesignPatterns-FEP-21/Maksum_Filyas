# ПАТЕРН "СТРАТЕГІЯ" - КОНКРЕТНА СТРАТЕГІЯ
from typing import List
from .base import WeatherStrategy
from app.db.models import Activity, UserPreferences
from app.core.logger import logger

class RainyWeatherStrategy(WeatherStrategy):
    """
    Стратегія для дощової погоди.
    Пропонує активності в приміщенні. 
    """
    
    def get_activities(self, preferences: UserPreferences) -> List[Activity]:
        activities = []
        
        # 1. Робота по дому (indoor / productive) 
        if "productive" in preferences.preferred_types or "indoor" in preferences.preferred_types:
             activities.append(Activity(name="Робота по дому", type="indoor", priority=3))
        
        # 2. Навчання / Робота (productive) 
        if "learning" in preferences.preferred_types and "learning" not in preferences.avoid_types:
            activities.append(Activity(name="Навчання (онлайн-курс)", type="learning", priority=1))
            
        # 3. Перегляд фільму (relax)
        activities.append(Activity(name="Перегляд фільму", type="relax", priority=2))
        
        logger.info(f"RainyStrategy: generated {len(activities)} activities.")
        return activities