import logging
from typing import Dict, Any, Callable

logger = logging.getLogger(__name__)

class ActionUrlFactory:
    """
    Фабрика, що відповідає за створення URL-шляхів для
    різних дій пристрою.
    """
    def __init__(self):
        # 3. Реєструємо всі наші "стратегії" побудови URL
        # Це і є "Фабрика" - вона знає, яку функцію викликати для якої дії
        self._builders: Dict[str, Callable] = {
            "power": self._build_power_path,
            "set_volume": self._build_volume_path,
            "set_brightness": self._build_brightness_path,
            "position": self._build_position_path,
        }

    # 1. Створюємо приватні "будівельники" для кожної дії
    def _build_power_path(self, **kwargs) -> str:
        """Створює шлях для 'power'."""
        state = kwargs.get('state')
        if state is None:
            raise ValueError("Для 'power' потрібен 'state'")
        return f"/power/{state}"

    def _build_volume_path(self, **kwargs) -> str:
        """Створює шлях для 'set_volume'."""
        level = kwargs.get('level')
        if level is None:
            raise ValueError("Для 'set_volume' потрібен 'level'")
        return f"/volume/{level}"

    def _build_brightness_path(self, **kwargs) -> str:
        """Створює шлях для 'set_brightness'."""
        level = kwargs.get('level')
        if level is None:
            raise ValueError("Для 'set_brightness' потрібен 'level'")
        return f"/brightness/{level}"

    def _build_position_path(self, **kwargs) -> str:
        """Створює шлях для 'position'."""
        value = kwargs.get('value')
        if value is None:
            raise ValueError("Для 'position' потрібен 'value'")
        return f"/position/{value}"

    # 2. Створюємо головний "фабричний метод"
    def create_action_path(self, action: str, **kwargs) -> str:
        """
        Головний метод Фабрики.
        Знаходить потрібного "будівельника" і викликає його.
        """
        # Знаходимо потрібну функцію-будівельник у нашому реєстрі
        builder = self._builders.get(action)

        if not builder:
            # Якщо дія невідома, кидаємо помилку
            logger.warning(f"Невідома дія '{action}'")
            raise ValueError(f"Невідомий тип дії: {action}")
        
        # Викликаємо знайдену функцію (напр., _build_power_path) з параметрами
        return builder(**kwargs)