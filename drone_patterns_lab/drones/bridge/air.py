from drones.bridge.base import MovementImplementor
from drones.utils.math_utils import Coordinate
from drones.utils.logger import setup_logger

logger = setup_logger("AirPlatform")

class AirPlatform(MovementImplementor):
    def takeoff(self):
        logger.info("AirPlatform: Пропелери розкручуються. Зліт на висоту зависання.")

    def land(self):
        logger.info("AirPlatform: Шасі випущено. М'яка посадка.")

    def move_to(self, coord: Coordinate):
        logger.info(f"AirPlatform: Політ до {coord} на крейсерській швидкості.")

    def adjust_course(self, vector: Coordinate):
        logger.info(f"AirPlatform: Зміна тангажу/крену на {vector}.")