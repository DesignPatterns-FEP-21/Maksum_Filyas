from drones.template.base import DroneMission
from drones.utils.logger import setup_logger

logger = setup_logger("RescueMission")

class RescueMission(DroneMission):
    """
    Рятувальна місія.
    Використовує тепловізори для пошуку людей або тварин у важкодоступних місцях.
    """
    
    def perform_payload_action(self):
        logger.info("Rescue: Scanning thermal signatures...")
        
        # Симуляція пошуку
        logger.info("Rescue: Thermal hotspot detected at coordinates.")
        
        self.results["survivors_found"] = 1
        self.results["location_coordinates"] = {"lat": 49.8, "lon": 24.0}