from drones.strategy.base import ReactionStrategy
from drones.utils.logger import setup_logger
from drones.utils.math_utils import Coordinate

logger = setup_logger("WaveReaction")

class WaveReaction(ReactionStrategy):
    """
    Стратегія реакції на хвилі.
    Якщо хвилі високі, дрон намагається стабілізуватися або спливти вище.
    """

    def react(self, mission_context, reading: dict):
        wave_height = reading.get("wave_height", 0)
        
        if wave_height > 2.5:
            logger.warning(f"Стратегія: Високі хвилі ({wave_height:.2f}м)! Стабілізація позиції.")
            mission_context.controller.adjust_course(Coordinate(1, 1, 0))
        else:
            logger.info(f"Стратегія: Море спокійне ({wave_height:.2f}м). Продовжуємо.")