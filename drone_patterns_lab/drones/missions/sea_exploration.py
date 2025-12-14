from drones.template.base import DroneMission
from drones.utils.logger import setup_logger

logger = setup_logger("SeaExplorationMission")

class SeaExplorationMission(DroneMission):
    """
    Місія для дослідження морського дна.
    Використовує сонар для картування або пошуку об'єктів під водою.
    """
    
    def perform_payload_action(self):
        logger.info("Морська розвідка: Активація сонару...")
        # Симуляція сканування
        logger.info("Морська розвідка: Картування морського дна.")
        
        self.results["depth_max"] = 150
        self.results["objects_found"] = ["Shipwreck_fragment", "Coral_reef"]