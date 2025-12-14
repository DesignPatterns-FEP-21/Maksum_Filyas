import unittest
from unittest.mock import MagicMock
from drones.cor.reroute_handler import ReRouteHandler

class TestChainOfResponsibility(unittest.TestCase):
    
    def setUp(self):
        self.handler = ReRouteHandler()
        self.mock_context = MagicMock()

    def test_handle_known_issue(self):
        """ReRouteHandler має вирішити проблему 'obstacle'."""
        result = self.handler.handle("obstacle_detected", self.mock_context)
        self.assertTrue(result) # True означає "оброблено"
        self.mock_context.controller.adjust_course.assert_called()

    def test_pass_unknown_issue(self):
        """Невідома проблема має бути передана далі (повернути False, бо next немає)."""
        result = self.handler.handle("low_battery", self.mock_context)
        self.assertFalse(result)