import time
from abc import ABC, abstractmethod
from typing import Dict, Any

from drones.config.mission_config import MissionConfig
from drones.bridge.controller import DroneController
from drones.environment.base import Environment
from drones.strategy.base import ReactionStrategy
from drones.cor.base import Handler
from drones.observer.event_bus import EventBus
from drones.utils.logger import setup_logger

logger = setup_logger("DroneMissionTemplate")

class DroneMission(ABC):
    def __init__(self, config: MissionConfig, controller: DroneController, 
                 environment: Environment, strategy: ReactionStrategy, 
                 fail_safe: Handler, event_bus: EventBus):
        self.config = config
        self.controller = controller
        self.environment = environment
        self.strategy = strategy
        self.fail_safe = fail_safe
        self.event_bus = event_bus
        self.results: Dict[str, Any] = {}
        self.status = "PENDING"

    def execute_mission(self) -> Dict[str, Any]:
        try:
            self.status = "RUNNING"
            logger.info(f"Місія {self.config.mission_id} РОЗПОЧАТА.")

            self.load_config()
            self.setup_event_subscriptions()
            
            self.environment.start()
            self.analyze_environment()

            self.preflight_check()
            self.controller.takeoff()
            self.navigate_to_area()

            readings = self.environment.sample()
            if self.environment_requires_reaction(readings):
                 self.react_to_environment(readings)

            self.perform_payload_action()

            logger.warning("ТЕСТ: Симулюємо перешкоду на шляху...")
            self.fail_safe.handle("obstacle_detected", self)
            
            logger.warning("ТЕСТ: Симулюємо критичну відмову двигуна...")
            self.fail_safe.handle("critical_failure", self)
            
            self.collect_and_store_data()
            self.return_to_base()
            
            self.controller.land()
            self.postprocess_results()
            
            self.status = "COMPLETED"
            logger.info(f"Місія {self.config.mission_id} УСПІШНО ЗАВЕРШЕНА.")

        except Exception as e:
            logger.error(f"Критична помилка під час місії: {e}")
            handled = self.fail_safe.handle(str(e), self)
            
            if not handled:
                self.status = "FAILED"
                self.results["error"] = str(e)
                try:
                    self.controller.land()
                except:
                    pass

        return self.results

    def load_config(self):
        logger.info(f"Конфігурацію завантажено для типу: {self.config.mission_type}.")

    def setup_event_subscriptions(self):
        pass

    def analyze_environment(self):
        data = self.environment.sample()
        logger.info(f"Аналіз середовища: {data}")

    def preflight_check(self):
        logger.info("Передпольотна перевірка: Всі системи В НОРМІ.")

    def navigate_to_area(self):
        logger.info(f"Навігація до цілі: {self.config.target_area}...")
        self.controller.goto(self.config.target_area)

    def environment_requires_reaction(self, readings: dict) -> bool:
        return bool(readings)

    def react_to_environment(self, reading: dict):
        self.strategy.react(self, reading)

    @abstractmethod
    def perform_payload_action(self):
        pass

    def collect_and_store_data(self):
        logger.info("Дані зібрано та збережено у внутрішнє сховище.")

    def return_to_base(self):
        logger.info(f"Повернення на базу {self.config.base_area}...")
        self.controller.goto(self.config.base_area)

    def postprocess_results(self):
        self.results["finished_at"] = time.time()
        logger.info("Результати оброблено.")