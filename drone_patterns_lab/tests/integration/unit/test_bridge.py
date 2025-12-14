import unittest
from unittest.mock import MagicMock
from drones.bridge.controller import DroneController
from drones.utils.math_utils import Coordinate

class TestBridgePattern(unittest.TestCase):
    
    def setUp(self):
        self.mock_impl = MagicMock()
        self.controller = DroneController(self.mock_impl)

    def test_takeoff_delegation(self):
        """Перевіряє, що контролер викликає takeoff у платформи."""
        self.controller.takeoff()
        self.mock_impl.takeoff.assert_called_once()

    def test_goto_coordinates(self):
        """Перевіряє передачу координат."""
        target = Coordinate(10, 20, 5)
        self.controller.goto(target)
        self.mock_impl.move_to.assert_called_with(target)