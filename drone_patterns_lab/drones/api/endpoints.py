import uuid
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from drones.factory.mission_factory import MissionFactory
from drones.utils.logger import setup_logger

logger = setup_logger("API_Endpoints")

router = APIRouter()

# --- Сховище в пам'яті  ---
MISSION_STORE: Dict[str, Dict[str, Any]] = {}

# --- Pydantic моделі для валідації вхідних даних ---
class MissionRequest(BaseModel):
    """Модель запиту для запуску місії."""
    mission_type: str      
    platform_type: str      
    environment_type: str   
    parameters: Dict[str, Any] = {} 

class MissionResponse(BaseModel):
    """Модель відповіді після створення місії."""
    mission_id: str
    status: str

def run_mission_background(mission_id: str, config_dict: dict):
    """
    Виконує місію у фоновому потоці, щоб не блокувати API.
    """
    try:
        logger.info(f"Background: Preparing mission {mission_id}...")
        
        # 1. Створення місії через Фабрику 
        # додаємю ID в конфіг, щоб фабрика знала його
        config_dict["mission_id"] = mission_id
        mission = MissionFactory.create_mission(config_dict)
        
        # Оновлює статус
        MISSION_STORE[mission_id]["status"] = "RUNNING"
        # 2. Виконання місії 
        result = mission.execute_mission()
        
        # 3. Збереження результату
        MISSION_STORE[mission_id]["status"] = "COMPLETED"
        MISSION_STORE[mission_id]["result"] = result
        logger.info(f"Background: Mission {mission_id} completed successfully.")
        
    except Exception as e:
        logger.error(f"Background: Mission {mission_id} failed. Error: {e}")
        MISSION_STORE[mission_id]["status"] = "FAILED"
        MISSION_STORE[mission_id]["error"] = str(e)

# Endpoints

@router.post("/mission/run", response_model=MissionResponse)
async def run_mission(request: MissionRequest, background_tasks: BackgroundTasks):
    """
    Запускає нову місію.
    """
    mission_id = str(uuid.uuid4())
    
    # Перетворює  модель у словник
    cfg_dict = request.model_dump()
    
    # Ініціалізує запис у сховищі
    MISSION_STORE[mission_id] = {
        "status": "PENDING",
        "config": cfg_dict,
        "result": None
    }
    
    # Додає завдання у фонові процеси FastAPI
    background_tasks.add_task(run_mission_background, mission_id, cfg_dict)
    
    logger.info(f"API: Received request to run mission {mission_id}")
    return {"mission_id": mission_id, "status": "PENDING"}

@router.get("/mission/status/{mission_id}")
async def get_status(mission_id: str):
    """
    Отримати поточний статус місії за ID.
    [cite: 125]
    """
    mission_data = MISSION_STORE.get(mission_id)
    
    if not mission_data:
        raise HTTPException(status_code=404, detail="Mission not found")
    
    return {
        "mission_id": mission_id,
        "status": mission_data["status"]
    }

@router.get("/mission/result/{mission_id}")
async def get_result(mission_id: str):
    """
    Отримати результати виконаної місії.
    [cite: 126]
    """
    mission_data = MISSION_STORE.get(mission_id)
    
    if not mission_data:
        raise HTTPException(status_code=404, detail="Mission not found")
        
    if mission_data["status"] != "COMPLETED":
        return {
            "mission_id": mission_id,
            "status": mission_data["status"],
            "message": "Mission results are not ready yet."
        }
    
    return {
        "mission_id": mission_id,
        "result": mission_data.get("result")
    }