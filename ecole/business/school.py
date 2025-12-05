# school.py
# -*- coding: utf-8 -*-

from daos.course_dao import CourseDao
from daos.teacher_dao import TeacherDao
from daos.student_dao import StudentDao
from daos.address_dao import AddressDao

class School:
    def __init__(self):
        # Créer les DAOs
        self.address_dao = AddressDao()
        self.student_dao = StudentDao()
        self.teacher_dao = TeacherDao()
        self.course_dao = CourseDao()

        # Charger toutes les données
        self.addresses = self.address_dao.read_all()
        self.students = self.student_dao.read_all()
        self.teachers = self.teacher_dao.read_all()
        self.courses = self.course_dao.read_all()

    def display_all_data(self):
        """Affiche toutes les données de l'école"""
        print("=" * 50)
        print("ADDRESSES:")
        print("=" * 50)
        for addr in self.addresses:
            print(f"ID: {addr.id}, {addr}")

        print("\n" + "=" * 50)
        print("STUDENTS:")
        print("=" * 50)
        for student in self.students:
            print(f"N°{student.student_nbr}: {student}")

        print("\n" + "=" * 50)
        print("TEACHERS:")
        print("=" * 50)
        for teacher in self.teachers:
            print(f"ID{teacher.id}: {teacher}")

        print("\n" + "=" * 50)
        print("COURSES:")
        print("=" * 50)
        for course in self.courses:
            print(f"\n{course.name} (ID: {course.id})")
            print(f"Du {course.start_date} au {course.end_date}")
            if course.teacher:
                print(f"Enseignant: {course.teacher.first_name} {course.teacher.last_name}")
            if course.students_taking_it:
                print("Étudiants inscrits:")
                for student in course.students_taking_it:
                    print(f"  - {student.first_name} {student.last_name} (N°{student.student_nbr})")

    def display_stats(self):
        """Affiche les statistiques"""
        print("\n" + "=" * 50)
        print("STATISTIQUES DE L'ÉCOLE")
        print("=" * 50)
        print(f"Nombre d'adresses: {len(self.addresses)}")
        print(f"Nombre d'étudiants: {len(self.students)}")
        print(f"Nombre d'enseignants: {len(self.teachers)}")
        print(f"Nombre de cours: {len(self.courses)}")

    """
    def init_static(self) -> None:
        #Initialisation d'un jeu de test pour l'école.
        
        # création des étudiants et rattachement à leur adresse
        paul: Student    = Student('Paul', 'Dubois', 12)
        valerie: Student = Student('Valérie', 'Dumont', 13)
        louis: Student   = Student('Louis', 'Berthot', 11)

        paul.address    = Address('12 rue des Pinsons', 'Castanet', 31320)
        valerie.address = Address('43 avenue Jean Zay', 'Toulouse', 31200)
        louis.address   = Address('7 impasse des Coteaux', 'Cornebarrieu', 31150)

        # ajout de ceux-ci à l'école
        for student in [paul, valerie, louis]:
            self.add_student(student)

        # création des cours
        francais: Course = Course("Français", date(2024, 1, 29),
                                              date(2024, 2, 16))
        histoire: Course = Course("Histoire", date(2024, 2, 5),
                                              date(2024, 2, 16))
        geographie: Course = Course("Géographie", date(2024, 2, 5),
                                                  date(2024, 2, 16))
        mathematiques: Course = Course("Mathématiques", date(2024, 2, 12),
                                                        date(2024, 3, 8))
        physique: Course = Course("Physique", date(2024, 2, 19),
                                              date(2024, 3, 8))
        chimie: Course = Course("Chimie", date(2024, 2, 26),
                                          date(2024, 3, 15))
        anglais: Course = Course("Anglais", date(2024, 2, 12),
                                            date(2024, 2, 24))
        sport: Course = Course("Sport", date(2024, 3, 4),
                                        date(2024, 3, 15))

        # ajout de ceux-ci à l'école
        for course in [francais, histoire, geographie, mathematiques,
                       physique, chimie, anglais, sport]:
            self.add_course(course)

        # création des enseignants
        victor  = Teacher('Victor', 'Hugo', 23, date(2023, 9, 4))
        jules   = Teacher('Jules', 'Michelet', 32, date(2023, 9, 4))
        sophie  = Teacher('Sophie', 'Germain', 25, date(2023, 9, 4))
        marie   = Teacher('Marie', 'Curie', 31, date(2023, 9, 4))
        william = Teacher('William', 'Shakespeare', 34, date(2023, 9, 4))
        michel  = Teacher('Michel', 'Platini', 42, date(2023, 9, 4))

        # ajout de ceux-ci à l'école
        for teacher in [victor, jules, sophie, marie, william, michel]:
            self.add_teacher(teacher)

        # association des élèves aux cours qu'ils suivent
        for course in [geographie, physique, anglais]:
            paul.add_course(course)

        for course in [francais, histoire, chimie]:
            valerie.add_course(course)

        for course in [mathematiques, physique, geographie, sport]:
            louis.add_course(course)

        # association des enseignants aux cours qu'ils enseignent
        victor.add_course(francais)

        jules.add_course(histoire)
        jules.add_course(geographie)

        sophie.add_course(mathematiques)

        marie.add_course(physique)
        marie.add_course(chimie)

        william.add_course(anglais)

        michel.add_course(sport)
    """
