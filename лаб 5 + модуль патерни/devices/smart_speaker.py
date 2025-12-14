from fastapi import FastAPI, HTTPException # Імпортуємо FastAPI для створення веб-сервера
from pydantic import BaseModel 
from typing import Dict, Any
import uvicorn # Імпортує uvicorn для запуску сервера
from devices.base_device import Device 

class SpeakerState(BaseModel): # Клас, що описує пам'ять або стан колонки
    is_on: bool = False 
    volume: int = 50 
    playing: bool = False # 
    current_track: str = "" 

class SmartSpeakerDevice(Device): # Клас розумної колонки, наслідує Device
    def __init__(self, device_id: str, host="127.0.0.1", port=8001):
        super().__init__(device_id, host, port) 
        self.state = SpeakerState() 
        self.app = FastAPI(title=f"Smart Speaker {device_id}") # Створює окремий FastAPI-додаток
        self._setup_routes() # Налаштовує URL-адреси (ендпоінти)

    def _setup_routes(self): # Метод для налаштування ендпоінтів
        app = self.app # Отримує доступ до нашого FastAPI-додатку

        @app.get("/status") # Створюємо GET-ендпоінт /status
        async def get_status():
            return self.get_status()

        @app.post("/power/{state}") # Створює POST-ендпоінт /power/on або /power/off
        async def set_power(state: str): 
            if not self.perform_action("power", state=state): 
                raise HTTPException(status_code=400, detail="Invalid power state") 
            return {"status": "success"} 

        # Додамо ендпоінт для гучності, щоб контролер міг ним керувати
        @app.post("/volume/{level}") # Створюємо POST-ендпоінт /volume/50
        async def set_volume(level: int): 
            if not self.perform_action("set_volume", level=level):
                raise HTTPException(status_code=400, detail="Invalid volume level") 
            return {"status": "success"} 

    def get_status(self) -> Dict[str, Any]:
        return { 
            "device_id": self.device_id,
            "type": "smart_speaker",
            "is_on": self.state.is_on, # Беремо дані з self.state
            "volume": self.state.volume, # Беремо дані з self.state
            "playing": self.state.playing,
            "current_track": self.state.current_track,
            "connection": f"{self.host}:{self.port}"
        }

    def perform_action(self, action: str, **kwargs) -> bool: # мозок пристрою
        if action == "power": 
            state = kwargs.get("state") 
            if state == "on": 
                self.state.is_on = True 
                return True 
            elif state == "off": 
                self.state.is_on = False
                self.state.playing = False 
                return True 
        elif action == "set_volume": 
            level = kwargs.get("level")
            if 0 <= level <= 100: 
                self.state.volume = level 
                return True 
        return False

    def run_server(self):
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
    
    speaker = SmartSpeakerDevice("speaker_001") 
    speaker.run_server() 

  