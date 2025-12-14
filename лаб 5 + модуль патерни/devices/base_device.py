#Цей файл визначає (Device), всі пристрої мати однакові функції (як-от get_status), 
# та обгортку (LoggingDeviceDecorator), яка записує їхні дії в лог.
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any
 
logger = logging.getLogger(__name__)

class Device(ABC): 
    """
    Будь-який клас, який хоче називатися 'Пристроєм',
    ПОВИНЕН мати методи get_status() та perform_action()."
    """
    def __init__(self, device_id: str, host: str, port: int):
        self.device_id = device_id
        self.host = host
        self.port = port
        self.base_url = f"http://{host}:{port}" # Створює зручну URL-адресу

    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        pass #дочірні класи повинні реалізуваит цей метод

    @abstractmethod
    def perform_action(self, action: str, **kwargs) -> bool:
        pass

    def run_server(self):
        pass

class LoggingDeviceDecorator(Device):
    
    def __init__(self, wrapped_device: Device):
        self._wrapped_device = wrapped_device
        # Ми також копіюємо атрибути (id, host, port) з реального об'єкта  у сам Декоратор. Це потрібно, щоб Фасад міг отримати
        # base_url з Декоратора, ніби це реальний пристрій.
        super().__init__(
            wrapped_device.device_id,
            wrapped_device.host,
            wrapped_device.port
        )

    def get_status(self) -> Dict[str, Any]:
        # Перевизначений метод 'get_status'. відбувається "декорування".
        logger.info(f"[LOG] Отримання статусу для {self.device_id}") #логування
        return self._wrapped_device.get_status() # 2. Викликаємо оригінальний метод на  об'єкті

    def perform_action(self, action: str, **kwargs) -> bool:
       # Перевизначений метод 'perform_action'.
        logger.info(f"[LOG] Виконання дії '{action}' на {self.device_id} з {kwargs}")
        result = self._wrapped_device.perform_action(action, **kwargs)  # Викликає оригінальний метод:
        logger.info(f"[LOG] Дія '{action}' на {self.device_id} завершилась: {result}")
        return result

    def __getattr__(self, name):
       # виклик неіснуючого методу цей метод автоматично перенаправить виклик на 'self._wrapped_device'.
        return getattr(self._wrapped_device, name)