from abc import ABC, abstractmethod
from sessions import LectureSession, PracticalSession, LabSession

# Базова фабрика (Factory Method)
class SessionFactory(ABC):
    @abstractmethod
    def create_session(self, time: str, room: str, teacher):
        pass

# Фабрика для лекцій
class LectureFactory(SessionFactory):
    def create_session(self, time: str, room: str, teacher):
        if not teacher.can_give_lecture():
            raise ValueError(f"{teacher.name} не може читати лекції")
        return LectureSession(time, room, teacher)

# Фабрика для практичних
class PracticalFactory(SessionFactory):
    def create_session(self, time: str, room: str, teacher):
        if not teacher.can_lead_practical():
            raise ValueError(f"{teacher.name} не може проводити практики")
        return PracticalSession(time, room, teacher)

# Приклад нової фабрики для лабораторних
class LabFactory(SessionFactory):
    def create_session(self, time: str, room: str, teacher):
        return LabSession(time, room, teacher)
