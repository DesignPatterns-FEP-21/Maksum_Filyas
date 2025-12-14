from drones.strategy.base import ReactionStrategy
from typing import Dict, Any
from drones.utils.logger import setup_logger
from drones.utils.math_utils import Coordinate

logger = setup_logger("CrackReaction")

class CrackReaction(ReactionStrategy):
    """
    Стратегія реакції на виявлення тріщин.
    При виявленні дефекту дрон уповільнюється або наближається для детального сканування.
    """
    def react(self, mission_context, reading: Dict[str, Any]):
        crack_depth = reading.get("crack_depth", 0)
        
        if crack_depth > 0:
            logger.info(f"Strategy: Crack detected (depth {crack_depth}mm). Approaching for macro scan.")
            # Наближаємось до поверхні (z = -0.5 метра)
            mission_context.controller.adjust_course(Coordinate(0, 0, -0.5))