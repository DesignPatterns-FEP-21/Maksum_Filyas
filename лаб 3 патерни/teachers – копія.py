from abc import ABC, abstractmethod

class Teacher(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def can_give_lecture(self): pass

    @abstractmethod
    def can_lead_practical(self): pass


class Lecturer(Teacher):
    def can_give_lecture(self): return True
    def can_lead_practical(self): return False


class Assistant(Teacher):
    def can_give_lecture(self): return False
    def can_lead_practical(self): return True


class ExternalMentor(Teacher):
    def can_give_lecture(self): return False
    def can_lead_practical(self): return False