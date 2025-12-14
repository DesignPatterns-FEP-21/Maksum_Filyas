from abc import ABC, abstractmethod

# Базовий клас для курсових робіт
class CourseWork(ABC):
    def __init__(self, supervisor):
        self.supervisor = supervisor

    @abstractmethod
    def submit(self):
        pass

# Курсові з різними форматами здачі
class OnlineSubmission(CourseWork):
    def submit(self):
        return "Курсова здана онлайн"

class GitHubSubmission(CourseWork):
    def submit(self):
        return "Курсова здана очно"

class OralDefense(CourseWork):
    def submit(self):
        return "Курсова захищена усно"