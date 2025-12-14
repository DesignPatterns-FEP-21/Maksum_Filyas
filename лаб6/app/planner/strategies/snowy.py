# ПАТЕРН "СТРАТЕГІЯ" - КОНКРЕТНА СТРАТЕГІЯ
from typing import List
from .base import WeatherStrategy
from app.db.models import Activity, UserPreferences
from app.core.logger import logger

class SnowyWeatherStrategy(WeatherStrategy):
    """
    Стратегія для сніжної погоди. 
    Пропонує затишні домашні активності або специфічні зимові розваги.
    """
    
    def get_activities(self, preferences: UserPreferences) -> List[Activity]:
        activities = []
        
        # 1. Залишитися вдома (гарячий шоколад, фільм)
        activities.append(Activity(name="Залишитися вдома (фільм та какао)", type="relax", priority=1))

        # 2. Зліпити сніговика (outdoor)
        if "outdoor" in preferences.preferred_types and "outdoor" not in preferences.avoid_types:
            activities.append(Activity(name="Зліпити сніговика / Прогулянка", type="outdoor", priority=2))
            
        # 3. Розчистити сніг (productive/sport)
        if "productive" in preferences.preferred_types and "sport" not in preferences.avoid_types:
            activities.append(Activity(name="Розчистити сніг", type="productive", priority=3))
        
        logger.info(f"SnowyStrategy: generated {len(activities)} activities.")
        return activities