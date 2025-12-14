import json
import os
from typing import Dict, Any
from drones.utils.logger import setup_logger

logger = setup_logger("Persistence")

class PersistenceLayer:
    """
    Шар збереження даних.
    Симулює запис результатів місії JSON-файл
    """
    
    @staticmethod
    def save_results(mission_id: str, results: Dict[str, Any]):
        filename = f"mission_{mission_id}_results.json"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=4, default=str)
            logger.info(f"Persistence: Results saved successfully to {filename}")
        except Exception as e:
            logger.error(f"Persistence: Failed to save results. Error: {e}")