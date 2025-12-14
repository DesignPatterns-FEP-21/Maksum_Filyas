from drones.cor.base import Handler
from drones.utils.logger import setup_logger

logger = setup_logger("EmergencyLandHandler")

class EmergencyLandHandler(Handler):
    """
    Критичний обробник. Якщо ніхто не вирішив проблему, садить дрон.
    """
    def handle(self, issue: str, context) -> bool:
        logger.critical(f"CoR (Ланцюжок): КРИТИЧНА ПОМИЛКА ({issue}). АВАРІЙНА ПОСАДКА!")
        try:
            context.controller.land()
            logger.info("CoR: Аварійна посадка виконана.")
            return True
        except Exception as e:
            logger.error(f"CoR: Посадка не вдалася: {e}")
            return False