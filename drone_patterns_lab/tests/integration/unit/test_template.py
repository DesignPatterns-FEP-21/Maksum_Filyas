import unittest
from unittest.mock import MagicMock
from drones.template.base import DroneMission
from drones.config.mission_config import MissionConfig
from drones.utils.math_utils import Coordinate

# Створюємо фіктивну місію для тестування абстрактного класу
class TestMissionImpl(DroneMission):
    def perform_payload_action(self):
        self.results["action_performed"] = True

class TestTemplateMethod(unittest.TestCase):
    
    def setUp(self):
        # Мокаємо залежності, щоб тестувати тільки логіку шаблону
        self.mock_config = MissionConfig("id", "Test", "Air", "Air", Coordinate(0,0,0))
        self.mock_env = MagicMock()
        self.mock_controller = MagicMock()
        
        self.mission = TestMissionImpl(
            self.mock_config, self.mock_controller, self.mock_env, 
            MagicMock(), MagicMock(), MagicMock()
        )

    def test_execution_flow(self):
        """Перевіряє повний цикл виконання місії."""
        self.mission.execute_mission()
        
        # Перевіряємо ключові етапи
        self.mock_env.start.assert_called()      # Аналіз середовища був
        self.mock_controller.takeoff.assert_called() # Зліт був
        self.assertTrue(self.mission.results["action_performed"]) # Дія виконана
        self.assertEqual(self.mission.status, "COMPLETED") # Статус оновлено