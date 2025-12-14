from drones.cor.base import Handler
from drones.utils.logger import setup_logger

logger = setup_logger("SwarmReassignHandler")

class SwarmReassignHandler(Handler):
    """
    Обробник, що передає завдання іншому дрону у випадку відмови датчиків.
    """
    def handle(self, issue: str, context) -> bool:
        if "sensor_failure" in issue or "load_error" in issue:
            logger.warning(f"CoR: Hardware failure ({issue}). Requesting swarm support...")
            # Симуляція передачі завдання
            logger.info("CoR: Task reassigned to Drone-Backup-01. Mission logically saved.")
            return True
            
        return super().handle(issue, context)