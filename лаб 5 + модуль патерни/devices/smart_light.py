from fastapi import FastAPI, HTTPException # Імпортуємо FastAPI для створення веб-сервера
from pydantic import BaseModel # Імпортуємо BaseModel для опису стану
from typing import Dict, Any
import uvicorn # Імпортуємо uvicorn для запуску сервера
from devices.base_device import Device 

class LightState(BaseModel): # Клас, що описує "пам'ять" або стан світла
    is_on: bool = False 
    brightness: int = 100 

class SmartLightDevice(Device): # 
    def __init__(self, device_id: str, host="127.0.0.1", port=8002):
        super().__init__(device_id, host, port) # Викликаємо конструктор базового класу
        self.state = LightState() 
        self.app = FastAPI(title=f"Smart Light {device_id}") # Створює окремий FastAPI-додаток
        self._setup_routes() # Налаштовуємо URL-адреси (ендпоінти)

    def _setup_routes(self): # Метод для налаштування ендпоінтів
        app = self.app # Отримує доступ до FastAPI-додатку

        @app.get("/status") # Створює GET-ендпоінт /status
        async def get_status():
            return self.get_status() 

        @app.post("/power/{state}") # Створюємо POST-ендпоінт /power/on або /power/off
        async def set_power(state: str): 
            if not self.perform_action("power", state=state): # Викликає мозок пристрою
                raise HTTPException(status_code=400, detail="Invalid power state") 
            return {"status": "success"} 

        @app.post("/brightness/{level}") # Створюємо POST-ендпоінт /brightness/50
        async def set_brightness(level: int): 
            if not self.perform_action("set_brightness", level=level): # Викликає мозок
                raise HTTPException(status_code=400, detail="Invalid brightness level") 
            return {"status": "success"} 

    def get_status(self) -> Dict[str, Any]: # Реалізація "контракту" Device
        return { 
            "device_id": self.device_id,
            "type": "smart_light",
            "is_on": self.state.is_on, 
            "brightness": self.state.brightness, 
            "connection": f"{self.host}:{self.port}"
        }

    def perform_action(self, action: str, **kwargs) -> bool: 
        if action == "power": # Якщо команда - "power"
            state = kwargs.get("state") # Дістаємо параметр 'state'
            if state == "on": # Якщо команда "on"
                self.state.is_on = True # Змінюємо стан
                return True 
            elif state == "off": # Якщо команда "off"
                self.state.is_on = False # Змінює стан
                return True 
        elif action == "set_brightness": 
            level = kwargs.get("level") # Дістає параметр 'level'
            if 0 <= level <= 100: # Перевіряє, чи коректне значення
                self.state.brightness = level # Змінює стан
                return True 
        return False 

    def run_server(self): # Метод для запуску сервера
        uvicorn.run(self.app, host=self.host, port=self.port, log_level="info") 

if __name__ == "__main__":
    
    import logging
    logging.basicConfig(
        level=logging.INFO,
        filename="smart_app.log",
        filemode="a",
        format="%(asctime)s - %(processName)s - %(name)s - %(levelname)s - %(message)s",
        force=True
    )

    light = SmartLightDevice("light_001") 
    light.run_server() 