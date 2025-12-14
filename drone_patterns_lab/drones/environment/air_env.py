import random
from drones.environment.base import Environment

class AirEnvironment(Environment):
    """
    Середовище повітря.
    Генерує дані про вітер, видимість та температуру.  Може генерувати події 'wind_gust' або 'storm'.
    """
    
    def sample(self) -> dict:
        # Симуляція випадкових значень
        data = {
            "wind_speed": random.randint(0, 35),  # м/с
            "visibility": random.randint(20, 100), # %
            "temperature": random.randint(-10, 30) # °C
        }
        
        # Логіка генерації подій (Observer)
        if data["wind_speed"] > 25:
            self.publish_event("wind_gust", data)
        
        if data["visibility"] < 40:
            self.publish_event("low_visibility", data)
            
        return data