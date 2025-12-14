from drones.template.base import DroneMission
from drones.utils.logger import setup_logger

logger = setup_logger("PollutionMonitoringMission")

class PollutionMonitoringMission(DroneMission):
    """
    Екологічна місія.
    Заміряє рівень забруднення повітря або води за допомогою датчиків.
    """
    
    def perform_payload_action(self):
        logger.info("Pollution: Taking air samples...")
        
        # Симуляція аналізу
        logger.info("Pollution: Analyzing CO2 and particulate matter levels.")
        
        self.results["aqi_level"] = 105
        self.results["status"] = "Unhealthy for Sensitive Groups"