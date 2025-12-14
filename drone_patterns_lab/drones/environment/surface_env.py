import random
from drones.environment.base import Environment

class SurfaceEnvironment(Environment):
    """
    Наземне середовище.
    Генерує дані про нерівність поверхні та щільність перешкод.
    Генерує подію 'obstacle_detected'.
    """
    
    def sample(self) -> dict:
        data = {
            "roughness": random.randint(1, 10), # шкала 1-10
            "obstacle_density": random.random(), # 0.0 - 1.0
            "slope_angle": random.randint(0, 45) # градуси
        }
        
        # Симуляція виявлення перешкоди
        if random.random() < 0.3: # 30% шанс зустріти перешкоду
            self.publish_event("obstacle_detected", {"distance": random.randint(1, 10)})
            
        return data