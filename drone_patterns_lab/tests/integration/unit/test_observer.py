import unittest
from unittest.mock import MagicMock
from drones.observer.event_bus import EventBus
from drones.observer.events import EnvironmentEvent

class TestObserverPattern(unittest.TestCase):
    
    def test_subscription_and_publishing(self):
        """Підписник має отримати подію, на яку підписався."""
        bus = EventBus()
        mock_callback = MagicMock()
        
        # Підписуємось
        bus.subscribe("wind_gust", mock_callback)
        
        # Публікуємо подію
        event = EnvironmentEvent("wind_gust", {"speed": 30})
        bus.publish(event)
        
        # Перевіряємо отримання
        mock_callback.assert_called_once_with(event)

    def test_ignore_unsubscribed_events(self):
        """Підписник не має отримувати чужі події."""
        bus = EventBus()
        mock_callback = MagicMock()
        
        bus.subscribe("wind_gust", mock_callback)
        bus.publish(EnvironmentEvent("rain", {}))
        
        mock_callback.assert_not_called()