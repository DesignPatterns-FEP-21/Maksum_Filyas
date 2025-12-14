# Цей клас реалізує ДВА патерни:
# 1. ПАТЕРН "СТРАТЕГІЯ" - КОНТЕКСТ (CONTEXT) 
#    - Він містить посилання на об'єкт Стратегії.
#    - Він обирає, яку стратегію використати.
# 2. ПАТЕРН "СПОСТЕРІГАЧ" - КОНКРЕТНИЙ СПОСТЕРІГАЧ (OBSERVER) 
#    - Він реагує на оновлення від WeatherStation.
#
import asyncio
from typing import Optional
from app.db.models import Weather, Plan, UserPreferences
from app.db.mongodb import get_database
from app.core.logger import logger
from app.weather.weather_station import IWeatherObserver

# Імпортуємо всі стратегії
from .strategies.base import WeatherStrategy
from .strategies.sunny import SunnyWeatherStrategy
from .strategies.rainy import RainyWeatherStrategy
from .strategies.cloudy import CloudyWeatherStrategy
from .strategies.snowy import SnowyWeatherStrategy

class DayPlanner(IWeatherObserver):
    """
    Контекст для Стратегії та Спостерігач для Погоди.
    """
    
    _strategy: Optional[WeatherStrategy] = None
    _strategy_map: dict[str, WeatherStrategy] = {
        "Clear": SunnyWeatherStrategy(),
        "Clouds": CloudyWeatherStrategy(),
        "Rain": RainyWeatherStrategy(),
        "Drizzle": RainyWeatherStrategy(),
        "Thunderstorm": RainyWeatherStrategy(),
        "Snow": SnowyWeatherStrategy(),
        "Mist": CloudyWeatherStrategy(),
        "Haze": CloudyWeatherStrategy(),
        "Fog": CloudyWeatherStrategy(),
    }
    
    _default_strategy: WeatherStrategy = CloudyWeatherStrategy()

    def __init__(self, user_id: str):
        self.user_id = user_id # Імітуємо роботу для конкретного юзера
        logger.info(f"DayPlanner for user {user_id} initialized.")

    # --- Реалізація Патерну "Стратегія"  ---
    
    def set_strategy(self, strategy: WeatherStrategy):
        """Встановлює конкретну стратегію."""
        self._strategy = strategy
        logger.info(f"DayPlanner: Set strategy to {strategy.__class__.__name__}")

    def _select_strategy(self, weather: Weather):
        """
        Автоматично обирає стратегію на основі погодних умов.
        """
        # Обираємо стратегію з мапи
        strategy_instance = self._strategy_map.get(weather.condition, self._default_strategy)
        self.set_strategy(strategy_instance)

    async def generate_plan(self, weather: Weather, city: str) -> Optional[Plan]:
        """
        Генерує план, використовуючи обрану стратегію.
        """
        # 1. Обираємо стратегію
        self._select_strategy(weather)
        
        # 2. Отримуємо налаштування користувача (тут хардкод, в реальності - з БД)
        # [cite: 14]
        db = await get_database()
        prefs_data = await db["preferences"].find_one({"user_id": self.user_id})
        if not prefs_data:
            # Створюємо дефолтні, якщо немає
            prefs_data = {"user_id": self.user_id, "preferred_types": ["outdoor", "indoor", "learning"], "avoid_types": []}
            await db["preferences"].insert_one(prefs_data)
            
        preferences = UserPreferences(**prefs_data)
        
        # 3. Використовуємо стратегію для отримання активностей [cite: 37, 39]
        if not self._strategy:
            logger.error("Strategy not set!")
            return None
            
        activities = self._strategy.get_activities(preferences)
        
        # 4. Створюємо об'єкт Плану
        new_plan = Plan(
            user_id=self.user_id,
            location=city,
            weather=weather,
            activities=activities
        )
        return new_plan

    # --- Реалізація Патерну "Спостерігач"  ---

    def update(self, weather: Weather, city: str):
        """
        Метод, який викликає Суб'єкт (WeatherStation), коли погода змінюється.
        [cite: 50, 51]
        """
        logger.info(f"DayPlanner (Observer): Received weather update! {weather.condition} in {city}")
        
        # Запускаємо асинхронну задачу генерації та збереження плану
        # оскільки update() викликається синхронно з notify()
        asyncio.create_task(self._handle_update(weather, city))

    async def _handle_update(self, weather: Weather, city: str):
        """
        Асинхронний обробник оновлення погоди.
        Генерує новий план та зберігає його в MongoDB. [cite: 51]
        """
        try:
            # 1. Генеруємо новий план [cite: 51]
            new_plan = await self.generate_plan(weather, city)
            
            if new_plan:
                # 2. Зберігаємо план в MongoDB [cite: 23, 51]
                db = await get_database()
                plan_data = new_plan.dict()
                result = await db["plans"].insert_one(plan_data)
                logger.info(f"New plan {result.inserted_id} saved to MongoDB.")
                # [cite: 101, 102]
        except Exception as e:
            logger.error(f"Failed to handle weather update: {e}")

# Створюємо єдиний екземпляр планувальника (для простоти, для user_123)
day_planner_instance = DayPlanner(user_id="user_123")