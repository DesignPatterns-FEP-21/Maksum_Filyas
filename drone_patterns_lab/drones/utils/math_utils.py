import math

class Coordinate:
    """
    Клас для представлення точки у тривимірному просторі (x, y, z).
    Використовується для навігації та визначення положення дрона.
    """
    def __init__(self, x: float, y: float, z: float = 0.0):
        self.x = x
        self.y = y
        self.z = z
    
    def __repr__(self):
        return f"({self.x:.2f}, {self.y:.2f}, {self.z:.2f})"
    
    def distance_to(self, other: 'Coordinate') -> float:
        """Обчислює евклідову відстань до іншої точки."""
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2)