import unittest
from unittest.mock import MagicMock
from drones.strategy.wind_reaction import WindReaction
from drones.utils.math_utils import Coordinate

class TestStrategyPattern(unittest.TestCase):
    
    def setUp(self):
        self.strategy = WindReaction()
        self.mock_context = MagicMock() # Контекст місії

    def test_react_to_high_wind(self):
        """Якщо вітер > 20, дрон має знизитись."""
        reading = {"wind_speed": 25}
        self.strategy.react(self.mock_context, reading)
        
        # Перевіряємо, що викликано adjust_course з від'ємним Z
        args, _ = self.mock_context.controller.adjust_course.call_args
        self.assertTrue(args[0].z < 0) 

    def test_ignore_low_wind(self):
        """Якщо вітер слабкий, реакції не має бути."""
        reading = {"wind_speed": 5}
        self.strategy.react(self.mock_context, reading)
        self.mock_context.controller.adjust_course.assert_not_called()