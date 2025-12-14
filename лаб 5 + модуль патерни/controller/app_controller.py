from typing import Dict, List, Any
from controller.iot_facade import IOTFacade # Імпортує Фасад - міст до мікросервісів
from devices.base_device import Device, LoggingDeviceDecorator # Імпортує базовий клас і Декоратор логування
# Імпортуємо класи конкретних пристроїв
from devices.smart_speaker import SmartSpeakerDevice
from devices.smart_light import SmartLightDevice
from devices.smart_curtains import SmartCurtainsDevice

#логування - це запис інформації

class AppController:
    """
    Головний контролер додатку. 
    (РЕФАКТОРЕНА ВЕРСІЯ з універсальними методами)
    """
    def __init__(self):
        """Конструктор. Викликається при старті main.py."""
        self.facade = IOTFacade() # Створюємо екземпляр Фасаду
        self._register_default_devices() # Реєструє всі пристрої

    def _register_default_devices(self):
        """Ініціалізує та реєструє всі пристрої."""
        devices_to_register = [
            LoggingDeviceDecorator(SmartSpeakerDevice("speaker_001", "127.0.0.1", 8001)),
            LoggingDeviceDecorator(SmartLightDevice("light_001", "127.0.0.1", 8002)),
            LoggingDeviceDecorator(SmartCurtainsDevice("curtains_001", "127.0.0.1", 8003))
        ]
        
        for device in devices_to_register:
            self.facade.register_device(device)

    # --- НОВИЙ УНІВЕРСАЛЬНИЙ МЕТОД 1 ---
    def toggle_device(self, device_id: str) -> Dict[str, Any]:
        """
        Універсальний метод для перемикання (вкл/викл, відкр/закр).
        Він сам визначає, який пристрій і як перемикати.
        """
        status = self.facade.get_device_status(device_id)
        if not status:
            return {} # Повертаємо порожній словник, якщо статус не отримано

        new_state_command = None # Команда, яку треба надіслати ("on", "off", "open", "close")

        # --- Логіка для різних типів пристроїв ---
        if (device_id == "speaker_001" or device_id == "light_001") and "is_on" in status:
            # Логіка для пристроїв, що вмикаються/вимикаються
            new_state_command = "off" if status["is_on"] else "on"
            
        elif device_id == "curtains_001" and "is_open" in status:
            # Логіка для пристроїв, що відкриваються/закриваються
            new_state_command = "close" if status["is_open"] else "open"
        # --- Кінець логіки ---

        if new_state_command:
            # Надсилаємо універсальну 'power' команду з визначеним станом
            success = self.facade.perform_device_action(
                device_id, "power", state=new_state_command
            )
            if success:
                return self.facade.get_device_status(device_id) # Повертаємо оновлений статус

        return status # Повертаємо старий статус, якщо щось пішло не так
    
    def set_device_value(self, device_id: str, action: str, value: int) -> bool:
        """
        Універсальний метод для встановлення значень (гучність, яскравість, позиція).
        Він сам визначає, як назвати параметр ('level' чи 'value') для Фасаду.
        """
        kwarg_name = "level" # Більшість пристроїв очікують 'level'
        
        if action == "position":
            kwarg_name = "value" # Але штори очікують 'value'

        # Динамічно створюємо словник з параметром: {'level': 80} або {'value': 50}
        kwargs = {kwarg_name: value}
        
        # Передаємо дію і параметри у Фасад
        return self.facade.perform_device_action(device_id, action, **kwargs)

    # --- Загальні Методи (залишаються без змін) ---

    def get_all_status(self) -> List[Dict[str, Any]]:
        """Отримати статус всіх пристроїв"""
        return self.facade.get_all_status()

    def register_new_device(self, device: Device) -> str:
        """Зареєструвати новий пристрій (для динамічного додавання)"""
        return self.facade.register_device(device)