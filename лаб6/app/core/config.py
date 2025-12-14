#Цей файл завантажує секретні ключі та налаштування з файлу .env 
# і робить їх доступними для решти програми через єдиний об'єкт settings.

import os
from pydantic import BaseSettings
from dotenv import load_dotenv

# Завантажуємо змінні середовища з .env файлу
load_dotenv()

class Settings(BaseSettings):
    """
    Налаштування додатку, завантажені зі змінних середовища.
    """
    MONGO_URL: str = os.getenv("MONGO_URL", "mongodb://localhost:27017")
    DB_NAME: str = os.getenv("DB_NAME", "smart_planner_db")
    OPENWEATHER_API_KEY: str = os.getenv("OPENWEATHER_API_KEY")
    DEFAULT_CITY: str = os.getenv("DEFAULT_CITY", "Kyiv")

    class Config:
        case_sensitive = True

# Створюємо єдиний екземпляр налаштувань
settings = Settings()