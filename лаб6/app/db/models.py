#Цей файл визначає точну структуру (схеми) для всіх даних, 
# які програма використовує, наприклад, як виглядають налаштування користувача , 
# дані про погоду та самі щоденні плани .
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

# --- Моделі для Налаштувань Користувача  ---

class WorkingHours(BaseModel):
    start: int = Field(..., ge=0, le=23)
    end: int = Field(..., ge=0, le=23)

class UserPreferences(BaseModel):
    user_id: str = Field(..., example="user_123")
    preferred_types: List[str] = Field(default_factory=list, example=["outdoor", "learning"])
    avoid_types: List[str] = Field(default_factory=list, example=["sport"])
    working_hours: Optional[WorkingHours] = None
    weekend_mode: bool = Field(default=False)

# --- Моделі для Плану  ---

class Weather(BaseModel):
    condition: str = Field(..., example="Rainy") # [cite: 85]
    temperature: float = Field(..., example=12.0) # [cite: 86]
    description: Optional[str] = None

class Activity(BaseModel):
    name: str = Field(..., example="HouseWork") # [cite: 88]
    type: str = Field(..., example="indoor")
    priority: int = Field(default=3)

class Plan(BaseModel):
    user_id: str = Field(..., example="user_123")
    date: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
    location: str = Field(..., example="Berlin")
    weather: Weather
    activities: List[Activity] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)

# Модель для відповіді API 
class PlanInDB(Plan):
    id: str = Field(..., alias="_id")