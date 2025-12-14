from drones.bridge.base import MovementImplementor
from drones.utils.math_utils import Coordinate
from drones.utils.logger import setup_logger

logger = setup_logger("DroneController")

class DroneController:
    """
    Абстракція керування.
    Отримує команди від місії та делегує їх виконання конкретній платформі.
    Це дозволяє змінювати тип дрона без зміни коду місії.
    """

    
    def __init__(self, implementor: MovementImplementor):
        self.impl = implementor

    def takeoff(self):
        logger.info("Контролер: Відправлено команду на ЗЛІТ.")
        self.impl.takeoff()

    def land(self):
        logger.info("Контролер: Відправлено команду на ПОСАДКУ.")
        self.impl.land()

    def goto(self, coord: Coordinate):
        logger.info(f"Контролер: Курс на координати {coord}.")
        self.impl.move_to(coord)

    def adjust_course(self, vector: Coordinate):
        logger.info(f"Контролер: Коригування курсу на вектор {vector}.")
        self.impl.adjust_course(vector)