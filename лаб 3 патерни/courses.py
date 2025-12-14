from abc import ABC, abstractmethod
from factories import LectureFactory, PracticalFactory
from courseworks import OnlineSubmission, GitHubSubmission, OralDefense

# Abstract Factory для курсів
class CourseFactory(ABC):
    @abstractmethod
    def create_lecture(self, time, room, teacher): pass
    @abstractmethod
    def create_practical(self, time, room, teacher): pass
    @abstractmethod
    def create_coursework(self, mentor): pass

# Конкретна фабрика для курсу "Програмування"
class ProgrammingCourseFactory(CourseFactory):
    def create_lecture(self, time, room, teacher):
        return LectureFactory().create_session(time, room, teacher)
    def create_practical(self, time, room, teacher):
        return PracticalFactory().create_session(time, room, teacher)
    def create_coursework(self, mentor):
        return GitHubSubmission(mentor)

# Конкретна фабрика для курсу "Бази даних"
class DatabasesCourseFactory(CourseFactory):
    def create_lecture(self, time, room, teacher):
        return LectureFactory().create_session(time, room, teacher)
    def create_practical(self, time, room, teacher):
        return PracticalFactory().create_session(time, room, teacher)
    def create_coursework(self, mentor):
        return OnlineSubmission(mentor)

# Конкретна фабрика для курсу "Математика"
class MathCourseFactory(CourseFactory):
    def create_lecture(self, time, room, teacher):
        return LectureFactory().create_session(time, room, teacher)
    def create_practical(self, time, room, teacher):
        return PracticalFactory().create_session(time, room, teacher)
    def create_coursework(self, mentor):
        return OralDefense(mentor)