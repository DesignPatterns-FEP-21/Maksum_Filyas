from typing import Dict, Any
from drones.config.mission_config import MissionConfig
from drones.utils.math_utils import Coordinate
from drones.utils.logger import setup_logger

logger = setup_logger("ConfigLoader")

class ConfigLoader:
    """
    Клас для завантаження та валідації конфігурації місії.
    """
    
    @staticmethod
    def load_config(data: Dict[str, Any]) -> MissionConfig:
        try:
            # Витягує дані координат цілі 
            target_data = data.get("target_area", {})
            target_coord = Coordinate(
                x=target_data.get("x", 10.0),
                y=target_data.get("y", 10.0),
                z=target_data.get("z", 5.0)
            )

            # Витягує координати бази 
            base_data = data.get("base_area", {})
            base_coord = Coordinate(
                x=base_data.get("x", 0.0),
                y=base_data.get("y", 0.0),
                z=base_data.get("z", 0.0)
            )

            # Створюєоб'єкт конфігурації 
            config = MissionConfig(
                mission_id=data.get("mission_id", "unknown"),
                mission_type=data.get("mission_type", "Agriculture"),
                platform_type=data.get("platform_type", "Air"),
                environment_type=data.get("environment_type", "Air"),
                target_area=target_coord,
                base_area=base_coord,
                parameters=data.get("parameters", {})
            )
            
            logger.info(f"Config loaded successfully for mission: {config.mission_id}")
            return config
            
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            raise ValueError(f"Invalid configuration data: {e}")