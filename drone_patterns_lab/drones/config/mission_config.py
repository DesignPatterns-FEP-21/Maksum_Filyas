from dataclasses import dataclass, field
from typing import Dict, Any
from drones.utils.math_utils import Coordinate

@dataclass
class MissionConfig:
    """
    Клас даних (Data Class), що зберігає всі налаштування місії.
    Використовується для передачі параметрів між шарами API, Factory та Mission.[
    """
    mission_id: str
    mission_type: str       # Наприклад: "Agriculture"
    platform_type: str      # Наприклад: "Air"
    environment_type: str   # Наприклад: "Air"
    target_area: Coordinate # Куди летимо
    
    # Координати бази 
    base_area: Coordinate = field(default_factory=lambda: Coordinate(0, 0, 0))
    
    # Додаткові параметри (швидкість, тип сенсора)
    parameters: Dict[str, Any] = field(default_factory=dict)