import unittest
from drones.factory.mission_factory import MissionFactory

class TestMissionIntegration(unittest.TestCase):
    
    def test_full_agriculture_mission(self):
        """
        Тестує створення та виконання місії Agriculture від початку до кінця.
        Перевіряє, чи фабрика правильно зібрала об'єкт і чи місія повернула результат.
        """
        # Конфігурація, яку ми нібито отримали з API
        config_data = {
            "mission_type": "Agriculture",
            "platform_type": "Air",
            "environment_type": "Air",
            "target_area": {"x": 100, "y": 100, "z": 20}
        }
        
        # 1. Створення через фабрику
        mission = MissionFactory.create_mission(config_data)
        
        # 2. Виконання
        results = mission.execute_mission()
        
        # 3. Перевірка результатів
        self.assertEqual(mission.status, "COMPLETED")
        self.assertIn("crops_status", results) 
        
        # --- ВИПРАВЛЕНО ТУТ (Healthy -> Здорові) ---
        self.assertEqual(results["crops_status"], "Здорові") 

if __name__ == '__main__':
    unittest.main()