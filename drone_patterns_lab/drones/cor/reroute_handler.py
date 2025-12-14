from drones.cor.base import Handler
from drones.utils.logger import setup_logger
from drones.utils.math_utils import Coordinate

logger = setup_logger("ReRouteHandler")

class ReRouteHandler(Handler):
    """
    Обробник, що змінює маршрут при виявленні перешкод.
    """

    def handle(self, issue: str, context) -> bool:
        if "obstacle" in issue or "route_blocked" in issue:
            logger.warning(f"CoR (Ланцюжок): Виявлено перешкоду ({issue}). Спроба змінити маршрут...")
            # Логіка обходу: зміщує на 5 одиниць вбік
            context.controller.adjust_course(Coordinate(5, 5, 0))
            logger.info("CoR: Маршрут успішно змінено. Продовжуємо місію.")
            return True
        return super().handle(issue, context)