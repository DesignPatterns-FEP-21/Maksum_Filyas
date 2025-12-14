from typing import Dict, Any

from drones.factory.config_loader import ConfigLoader
from drones.utils.logger import setup_logger
from drones.observer.event_bus import EventBus

# Імпорти середовищ
from drones.environment import (
    AirEnvironment, SeaEnvironment, SurfaceEnvironment
)
# Імпорти платформ
from drones.bridge import (
    DroneController, AirPlatform, SeaPlatform, SurfacePlatform
)
# Імпорти стратегій (ЗВЕРНІТЬ УВАГУ НА NoReaction)
from drones.strategy.base import ReactionStrategy, NoReaction 
from drones.strategy import (
    WindReaction, WaveReaction, CrackReaction
)
# Імпорти CoR
from drones.cor import (
    EmergencyLandHandler, ReRouteHandler, AdjustAltitudeHandler, SwarmReassignHandler
)
# Імпорти місій
from drones.missions import (
    AgricultureMission, SeaExplorationMission, DefectsDetectionMission, 
    RescueMission, PollutionMonitoringMission
)

logger = setup_logger("MissionFactory")

class MissionFactory:
    """
    Центральна фабрика. Виправлена для використання NoReaction.
    """

    @staticmethod
    def create_mission(config_dict: Dict[str, Any]):
        logger.info("Factory: Starting mission assembly...")
        
        # 1. Завантаження
        config = ConfigLoader.load_config(config_dict)
        event_bus = EventBus()

        # --- Словники (Registry) ---
        env_map = {
            "Air": AirEnvironment,
            "Sea": SeaEnvironment,
            "Surface": SurfaceEnvironment
        }

        platform_map = {
            "Air": AirPlatform,
            "Sea": SeaPlatform,
            "Surface": SurfacePlatform
        }

        strategy_map = {
            "Air": WindReaction,
            "Sea": WaveReaction,
            # Surface тут немає, тому спрацює дефолт
        }

        mission_class_map = {
            "Agriculture": AgricultureMission,
            "SeaExploration": SeaExplorationMission,
            "DefectsDetection": DefectsDetectionMission,
            "Rescue": RescueMission,
            "PollutionMonitoring": PollutionMonitoringMission
        }

        # --- Створення об'єктів ---

        # 2. Середовище
        EnvClass = env_map.get(config.environment_type, SurfaceEnvironment)
        environment = EnvClass(event_bus)

        # 3. Платформа
        PlatformClass = platform_map.get(config.platform_type, SurfacePlatform)
        controller = DroneController(PlatformClass())

        # 4. Стратегія (ВИПРАВЛЕНО ТУТ)
        if config.mission_type == "DefectsDetection":
            strategy = CrackReaction()
        else:
            # Якщо для середовища немає стратегії, беремо NoReaction, а не абстрактний клас
            StrategyClass = strategy_map.get(config.environment_type, NoReaction)
            strategy = StrategyClass()

        # 5. CoR (Ланцюжок безпеки)
        emergency = EmergencyLandHandler()
        reroute = ReRouteHandler()
        reroute.set_next(AdjustAltitudeHandler())\
               .set_next(SwarmReassignHandler())\
               .set_next(emergency)
        fail_safe_chain = reroute

        # 6. Місія
        MissionClass = mission_class_map.get(config.mission_type, AgricultureMission)
        
        logger.info(f"Factory: Created {config.mission_type} mission.")
        
        return MissionClass(
            config=config,
            controller=controller,
            environment=environment,
            strategy=strategy,
            fail_safe=fail_safe_chain,
            event_bus=event_bus
        )