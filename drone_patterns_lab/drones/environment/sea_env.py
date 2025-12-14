import random
from drones.environment.base import Environment

class SeaEnvironment(Environment):
    """
    Морське середовище. Генерує дані про висоту хвиль, течію та солоність. Генерує подію 'high_waves'.
    """
    
    def sample(self) -> dict:
        data = {
            "wave_height": random.uniform(0, 6.0), # метри
            "current_speed": random.uniform(0, 10.0), # вузли
            "salinity": 35 # проміле (стала)
        }
        
        # Якщо хвилі занадто високі -> подія
        if data["wave_height"] > 4.0:
            self.publish_event("high_waves", data)
            
        return data