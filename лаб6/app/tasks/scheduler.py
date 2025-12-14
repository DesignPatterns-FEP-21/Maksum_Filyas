from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.core.config import settings
from app.core.logger import logger
from app.weather.weather_station import weather_station

# Створюємо екземпляр планувальника
scheduler = AsyncIOScheduler(timezone="UTC")

async def check_weather_job():
    """
    Фонове завдання, що періодично перевіряє погоду.
    
    """
    city = settings.DEFAULT_CITY
    logger.info(f"Scheduler: Running check_weather_job for {city}...")
    # fetch_weather() автоматично викличе notify() якщо погода змінилась 
    await weather_station.fetch_weather(city)

def start_scheduler():
    """Додає завдання в планувальник і запускає його."""
    try:
        scheduler.add_job(
            check_weather_job,
            trigger="interval",
            minutes=30,  #  (використовуємо 30 хв як приклад)
            id="weather_check",
            replace_existing=True
        )
        scheduler.start()
        logger.info("Background scheduler started. Weather check every 30 mins.")
    except Exception as e:
        logger.error(f"Failed to start scheduler: {e}")

def stop_scheduler():
    """Зупиняє планувальник."""
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Background scheduler stopped.")