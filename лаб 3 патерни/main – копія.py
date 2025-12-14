from teachers import Lecturer, Assistant, ExternalMentor
from courses import ProgrammingCourseFactory, DatabasesCourseFactory
from groups import StudentGroup

def main():
    lecturer = Lecturer("Др. Шевченко Іван")
    assistant = Assistant("Др. Марія Петренко")
    mentor = ExternalMentor("Індустріальний експерт")

    prog_factory = ProgrammingCourseFactory()
    db_factory = DatabasesCourseFactory()

    group1 = StudentGroup("ФеП-21")
    group2 = StudentGroup("ФеП-22")

    lecture1 = prog_factory.create_lecture("Пн 10:00", "101", lecturer)
    practical1 = prog_factory.create_practical("Вт 12:00", "Лаб1", assistant)
    coursework1 = prog_factory.create_coursework(mentor)

    group1.add_session(lecture1)
    group1.add_session(practical1)

    lecture2 = db_factory.create_lecture("Пн 10:00", "102", lecturer)
    practical2 = db_factory.create_practical("Ср 14:00", "Лаб2", assistant)
    coursework2 = db_factory.create_coursework(mentor)

    group2.add_session(lecture2)
    group2.add_session(practical2)


    print("Розклад для", group1.name)
    for s in group1.sessions:
        print(" ", s)
    print("Курсова:", coursework1.submit())

    print("\nРозклад для", group2.name)
    for s in group2.sessions:
        print(" ", s)
    print("Курсова:", coursework2.submit())


if __name__ == "__main__":
    main()