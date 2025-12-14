from abc import ABC, abstractmethod
from drones.utils.math_utils import Coordinate

class MovementImplementor(ABC):
    """
    Інтерфейс реалізації руху (Implementor).
    Визначає базові низькорівневі команди, які має підтримувати будь-яка платформа (повітряна, морська, наземна).
    """
    @abstractmethod
    def takeoff(self):
        """Запуск двигунів / Зліт."""
        pass

    @abstractmethod
    def land(self):
        """Зупинка / Посадка."""
        pass

    @abstractmethod
    def move_to(self, coord: Coordinate):
        """Рух до конкретної точки."""
        pass

    @abstractmethod
    def adjust_course(self, vector: Coordinate):
        """Коригування курсу."""
        pass