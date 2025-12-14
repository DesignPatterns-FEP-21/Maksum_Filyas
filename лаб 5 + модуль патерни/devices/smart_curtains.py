from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import uvicorn
from devices.base_device import Device 

class CurtainState(BaseModel): # описує стан або пам'ять пристрою
    is_open: bool = False
    position: int = 0  # 0 = закрито, 100 = повністю відкрито

class SmartCurtainsDevice(Device):
    
    def __init__(self, device_id: str, host="127.0.0.1", port=8003):
        super().__init__(device_id, host, port) # Викликає конструктор базового класу
        self.state = CurtainState() # Створюємекземпляр стану пам'ять
        self.app = FastAPI(title=f"Smart Curtains {device_id}") # Створює окремий FastAPI-додаток ТІЛЬКИ для цього пристрою
        self._setup_routes() # Налаштовуємо URL-адреси 

    def _setup_routes(self):
        """Налаштовує HTTP для цього мікросервісу."""
        app = self.app
        #POST — це команда "Візьми ці дані і щось з ними зроби"
        #GET — це команда "Просто дай мені інформацію".
        @app.get("/status")
        async def get_status():
            return self.get_status() # Викликає метод get_status

        @app.post("/power/{state}")
        async def set_power(state: str):
            if not self.perform_action("power", state=state): # Викликаємо наш логічний метод perform_action
                raise HTTPException(status_code=400, detail="Invalid curtain state")
            return {"status": "success"} 

        @app.post("/position/{value}")
        async def set_position(value: int):
            if not self.perform_action("position", value=value):
                raise HTTPException(status_code=400, detail="Invalid position")
            return {"status": "success"}

    def get_status(self) -> Dict[str, Any]:
        return {
            "device_id": self.device_id,
            "type": "smart_curtains",
            "is_open": self.state.is_open,
            "position": self.state.position,
            "connection": f"{self.host}:{self.port}"
        }

    def perform_action(self, action: str, **kwargs) -> bool:
        # Це - "мозок" пристрою, який змінює його стан.
        if action == "power":
            state = kwargs.get("state")  # Якщо команда - "power", дістаємо 'state' з kwargs
            if state == "open":
                self.state.is_open = True
                self.state.position = 100
                return True
            elif state == "close":
                self.state.is_open = False
                self.state.position = 0
                return True 
                
        elif action == "position":
            value = kwargs.get("value")
            if 0 <= value <= 100: # Перевіряємо, чи значення коректне (0-100)
                self.state.position = value
                self.state.is_open = value > 0 # Важлива логіка: якщо позиція > 0, штори вважаються відкритими
                return True 
        
        return False 

    def run_server(self):
        """Запускає цей конкретний мікросервіс."""
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
    
    curtains = SmartCurtainsDevice("curtains_001")
    curtains.run_server()