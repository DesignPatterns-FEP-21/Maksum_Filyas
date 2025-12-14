from drones.cor.base import Handler
from drones.utils.logger import setup_logger
from drones.utils.math_utils import Coordinate

logger = setup_logger("AdjustAltitudeHandler")

class AdjustAltitudeHandler(Handler):
    """
    Обробник, що змінює висоту при поганій видимості або штормі.
    """
    def handle(self, issue: str, context) -> bool:
        if "visibility" in issue or "weather" in issue:
            logger.warning(f"CoR: Weather/Visibility issue ({issue}). Adjusting altitude...")
            # Логіка: піднімає вище, де може бути краща видимість
            context.controller.adjust_course(Coordinate(0, 0, 10))
            logger.info("CoR: Altitude adjusted. Issue resolved.")
            return True
            
        return super().handle(issue, context)