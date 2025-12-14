from drones.strategy.base import ReactionStrategy
from drones.utils.logger import setup_logger
from drones.utils.math_utils import Coordinate

logger = setup_logger("WindReaction")

class WindReaction(ReactionStrategy):
    """
    Стратегія реакції на вітер.
    Якщо вітер занадто сильний, дрон знижує висоту для стабілізації.
    """
    
    def react(self, mission_context, reading: dict):
        wind_speed = reading.get("wind_speed", 0)
        
        if wind_speed > 20:
            logger.warning(f"Стратегія: УВАГА! Сильний вітер ({wind_speed} м/с)! Знижуємо висоту.")
            mission_context.controller.adjust_course(Coordinate(0, 0, -2))
        else:
            logger.info(f"Стратегія: Вітер в нормі ({wind_speed} м/с). Реакція не потрібна.")