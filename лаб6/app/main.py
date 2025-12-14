from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.routes import api_router
from app.db.mongodb import connect_to_mongo, close_mongo_connection
from app.tasks.scheduler import start_scheduler, stop_scheduler
from app.weather.weather_station import weather_station
from app.planner.day_planner import day_planner_instance
from app.core.logger import logger
from app.core.config import settings

# Створюємо додаток FastAPI
app = FastAPI(title="Smart Day Planner Service")

# Монтуємо статичні файли (CSS) 
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Обробники подій життєвого циклу додатку
@app.on_event("startup")
async def startup_event():
    """
    Виконується при старті додатку:
    1. Підключення до MongoDB 
    2. Запуск фонового планувальника [cite: 11]
    3. Прив'язка Спостерігача (Planner) до Суб'єкта (WeatherStation) [cite: 46-51]
    """
    logger.info("Application startup...")
    await connect_to_mongo()
    
    # ПРИВ'ЯЗКА СПОСТЕРІГАЧА
    weather_station.attach(day_planner_instance)
    
    start_scheduler()
    
    # Запускаємо першу перевірку погоди одразу при старті
    await weather_station.fetch_weather(settings.DEFAULT_CITY)


@app.on_event("shutdown")
async def shutdown_event():
    """Виконується при зупинці додатку."""
    logger.info("Application shutdown...")
    stop_scheduler()
    await close_mongo_connection()

# Включаємо роутер API
app.include_router(api_router, prefix="/api/v1")

@app.get("/", include_in_schema=False)
async def root_redirect():
    """Редирект з кореня на сторінку API."""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/api/v1/")