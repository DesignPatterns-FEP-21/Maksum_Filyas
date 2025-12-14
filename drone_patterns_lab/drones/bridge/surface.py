from drones.bridge.base import MovementImplementor
from drones.utils.math_utils import Coordinate
from drones.utils.logger import setup_logger

logger = setup_logger("SurfacePlatform")

class SurfacePlatform(MovementImplementor):
    def takeoff(self):
        logger.info("SurfacePlatform: Двигун запущено. Гальма відпущено.")

    def land(self):
        logger.info("SurfacePlatform: Гальма затиснуто. Двигун вимкнено.")

    def move_to(self, coord: Coordinate):
        logger.info(f"SurfacePlatform: Їдемо до {coord}, оминаючи рельєф.")

    def adjust_course(self, vector: Coordinate):
        logger.info(f"SurfacePlatform: Поворот коліс на {vector}.")