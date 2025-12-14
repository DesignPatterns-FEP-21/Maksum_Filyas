from typing import Any

class EnvironmentEvent:
    """
    Клас-контейнер для подій.
    Зберігає тип події (наприклад, 'wind_gust'), дані про неї та джерело походження.
    """
    def __init__(self, event_type: str, data: Any, source: str = "Unknown"):
        self.event_type = event_type
        self.data = data
        self.source = source

    def __repr__(self):
        return f"<Event {self.event_type} from {self.source}>"