#Цей файл визначає всі API-адреси (ендпоінти)  додатка, 
# обробляє запити до них (як-от отримання плану чи оновлення погоди ) і віддає головну HTML-сторінку.
from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List

from app.db.mongodb import get_database
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.db.models import Plan, PlanInDB, UserPreferences
from app.weather.weather_station import weather_station
from app.core.config import settings

api_router = APIRouter()

# Налаштування для HTML шаблонів
templates = Jinja2Templates(directory="frontend/templates")

@api_router.get("/", response_class=HTMLResponse, summary="Головна сторінка (Frontend)")
async def get_frontend_page(request: Request, db: AsyncIOMotorDatabase = Depends(get_database)):
    """
    Відображає простий HTML/CSS інтерфейс.
    """
    latest_plan_data = await db["plans"].find_one(
        {"user_id": "user_123"},
        sort=[("created_at", -1)]
    )
    
    plan = None
    if latest_plan_data:
        # Конвертуємо ObjectId в str перед валідацією Pydantic
        latest_plan_data["_id"] = str(latest_plan_data["_id"]) # <-- ВИПРАВЛЕНО 1
        plan = PlanInDB(**latest_plan_data)

    context = {
        "request": request,
        "current_weather": plan.weather if plan else "N/A",
        "current_plan": plan.activities if plan else [],
        "location": plan.location if plan else settings.DEFAULT_CITY
    }
    return templates.TemplateResponse("index.html", context)


@api_router.get("/plan", response_model=PlanInDB, summary="Отримати поточний план")
async def get_current_plan(db: AsyncIOMotorDatabase = Depends(get_database)):
    """
    Повертає останній згенерований план для користувача.
    """
    latest_plan_data = await db["plans"].find_one(
        {"user_id": "user_123"},
        sort=[("created_at", -1)]
    )
    if latest_plan_data:
        latest_plan_data["_id"] = str(latest_plan_data["_id"]) # <-- ВИПРАВЛЕНО 2
        return PlanInDB(**latest_plan_data)
    raise HTTPException(status_code=404, detail="Plan not found")

@api_router.post("/plan/refresh", summary="Примусово оновити погоду та план")
async def force_weather_update():
    """
    Примусово запускає перевірку погоди.
    """
    await weather_station.fetch_weather(settings.DEFAULT_CITY)
    return {"message": "Weather check triggered. Plan will update if conditions changed."}

@api_router.get("/plans/history", response_model=List[PlanInDB], summary="Переглянути збережені плани")
async def get_stored_plans(db: AsyncIOMotorDatabase = Depends(get_database)):
    """
    Повертає історію планів.
    """
    plans = []
    cursor = db["plans"].find({"user_id": "user_123"}).sort("created_at", -1).limit(10)
    async for plan_data in cursor:
        plan_data["_id"] = str(plan_data["_id"]) # <-- ВИПРАВЛЕНО 3
        plans.append(PlanInDB(**plan_data))
    return plans

@api_router.post("/preferences", response_model=UserPreferences, summary="Встановити вподобання користувача")
async def set_user_preferences(prefs: UserPreferences, db: AsyncIOMotorDatabase = Depends(get_database)):
    """
    Оновлює або створює налаштування для користувача.
    """
    # pydantic v1 .dict()
    await db["preferences"].update_one(
        {"user_id": prefs.user_id},
        {"$set": prefs.dict()},
        upsert=True
    )
    return prefs

@api_router.get("/preferences/{user_id}", response_model=UserPreferences, summary="Отримати вподобання користувача")
async def get_user_preferences(user_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    """
    Отримує налаштування для користувача.
    """
    prefs_data = await db["preferences"].find_one({"user_id": user_id})
    if prefs_data:
        return UserPreferences(**prefs_data)
    raise HTTPException(status_code=404, detail="Preferences not found")