from drones.bridge.base import MovementImplementor
from drones.utils.math_utils import Coordinate
from drones.utils.logger import setup_logger

logger = setup_logger("SeaPlatform")

class SeaPlatform(MovementImplementor):
    def takeoff(self):
        logger.info("SeaPlatform: Двигуни увімкнено. Вихід з доку.")

    def land(self):
        logger.info("SeaPlatform: Двигуни зупинено. Якір кинуто.")

    def move_to(self, coord: Coordinate):
        logger.info(f"SeaPlatform: Пливемо/Занурюємось до {coord}.")

    def adjust_course(self, vector: Coordinate):
        logger.info(f"SeaPlatform: Коригування керма/баласту на {vector}.")