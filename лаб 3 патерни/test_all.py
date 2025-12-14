import pytest
from factories import LectureFactory, PracticalFactory
from sessions import LectureSession, PracticalSession
from teachers import Lecturer, Assistant, ExternalMentor
from courseworks import OnlineSubmission, GitHubSubmission
from groups import StudentGroup

# ---------- UNIT TESTS ----------

# Перевірка: фабрика лекцій створює об'єкт LectureSession
def test_lecture_factory_creates_lecture():
    teacher = Lecturer("Dr. Smith")  # створюємо викладача
    session = LectureFactory().create_session("Mon 10:00", "101", teacher)  # створюємо лекцію
    assert isinstance(session, LectureSession)  # перевіряємо тип об'єкта

# Перевірка: фабрика практик створює об'єкт PracticalSession
def test_practical_factory_creates_practical():
    teacher = Assistant("Dr. Johnson")  # створюємо асистента
    session = PracticalFactory().create_session("Tue 12:00", "Lab1", teacher)  # створюємо практику
    assert isinstance(session, PracticalSession)  # перевіряємо тип об'єкта

# Перевірка: зовнішній ментор не може вести лекцію
def test_external_mentor_cannot_give_lecture():
    teacher = ExternalMentor("Industry Expert")  # зовнішній ментор
    with pytest.raises(ValueError):  # очікуємо помилку при спробі створити лекцію
        LectureFactory().create_session("Wed 14:00", "102", teacher)

# Інтеграційний тест: перевірка конфлікту розкладу в групі
def test_schedule_conflict_detection():
    group = StudentGroup("FEP-21")  # створюємо студентську групу
    t = Lecturer("Dr. Oleg")  # створюємо викладача
    lecture1 = LectureFactory().create_session("Mon 10:00", "101", t)  # перша лекція
    lecture2 = LectureFactory().create_session("Mon 10:00", "102", t)  # друга лекція у той же час
    group.add_session(lecture1)  # додаємо першу лекцію у розклад
    with pytest.raises(ValueError):  # очікуємо помилку через конфлікт часу
        group.add_session(lecture2)
