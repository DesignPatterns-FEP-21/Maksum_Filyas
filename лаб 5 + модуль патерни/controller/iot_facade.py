import requests
import logging
from typing import Dict, List, Any
from devices.base_device import Device
from controller.url_factory import ActionUrlFactory 

logger = logging.getLogger(__name__)

class IOTFacade:
    """
    Фасад, що абстрагує HTTP-комунікацію з мікросервісами.
    (Тепер використовує Фабрику для побудови URL)
    """
    def __init__(self):
        self.devices: Dict[str, Device] = {}
        self.client = requests.Session() 
        # Створюємо екземпляр нашої Фабрики
        self.url_factory = ActionUrlFactory()

    def register_device(self, device: Device) -> str:
        self.devices[device.device_id] = device
        logger.info(f"Пристрій {device.device_id} зареєстровано на {device.base_url}")
        return device.device_id

    def get_device_status(self, device_id: str) -> Dict[str, Any]:
        # ... (цей метод залишається без змін) ...
        device = self.devices.get(device_id)
        if not device:
            return {"error": "Device not found"}
        
        try:
            response = self.client.get(f"{device.base_url}/status", timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.RequestError as e:
            logger.error(f"Помилка запиту до {device_id}: {e}")
            return {"device_id": device_id, "type": "unknown", "connection": "error"}

    def get_all_status(self) -> List[Dict[str, Any]]:
        statuses = []
        for device_id in self.devices:
            status = self.get_device_status(device_id)
            statuses.append(status)
        return statuses

    def perform_device_action(self, device_id: str, action: str, **kwargs) -> bool:
        """Виконує дію на пристрої (з використанням Фабрики)."""

        device = self.devices.get(device_id) # 1. Знаходимо пристрій
        if not device:
            return False

        try:
            # 2. Використовуємо Фабрику, щоб отримати готовий URL-шлях
            #    Повністю позбулися блоку if/elif/else!
            action_path = self.url_factory.create_action_path(action, **kwargs)
            
            # 3. Будуємо повний URL
            url = f"{device.base_url}{action_path}"

            # 4. Надсилаємо HTTP POST-запит
            response = self.client.post(url, timeout=5)
            response.raise_for_status() # Перевіряємо на помилки
            
            # 5. Повертаємо True, якщо мікросервіс відповів {"status": "success"}
            return response.json().get("status") == "success"
        
        except ValueError as e:
            # Ця помилка прилетить з Фабрики, якщо дія невідома
            logger.error(f"Помилка створення URL: {e}")
            return False
        except requests.RequestError as e:
            # Ця помилка - від 'requests', якщо сервер недоступний
            logger.error(f"Помилка виконання дії {action} на {device_id}: {e}")
            return False