from abc import ABC, abstractmethod

# Базовий клас для всіх типів занять (лекція, практика, лаба)
class Session(ABC):
    def __init__(self, time: str, room: str, teacher):
        self.time = time
        self.room = room
        self.teacher = teacher

    @abstractmethod
    def __str__(self):
        pass

# Лекція, потребує викладача категорії Lecturer
class LectureSession(Session):
    def __str__(self):
        return f"Лекція {self.time} в ауд. {self.room}, викладач {self.teacher.name}"

# Практика, потребує викладача категорії Assistant
class PracticalSession(Session):
    def __str__(self):
        return f"Практика {self.time} в ауд. {self.room}, асистент {self.teacher.name}"

# Приклад розширення: Лабораторна (новий тип занять без змін у старих класах)
class LabSession(Session):
    def __str__(self):
        return f"Лабораторна {self.time} в ауд. {self.room}, викладач {self.teacher.name}"

