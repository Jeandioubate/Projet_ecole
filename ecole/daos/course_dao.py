# -*- coding: utf-8 -*-

"""
Classe Dao[Course]
"""

from models.course import Course
from daos.dao import Dao
from dataclasses import dataclass
from typing import Optional, List
from daos.teacher_dao import TeacherDao
from daos.student_dao import StudentDao


@dataclass
class CourseDao(Dao[Course]):
    def create(self, course: Course) -> int:
        """Crée en BD l'entité Course correspondant au cours course

        :param course: à créer sous forme d'entité Course en BD
        :return: l'id de l'entité insérée en BD (0 si la création a échoué)
        """
        ...
        try:
            if course.teacher is None or course.teacher.id is None:
                return 0

            with Dao.connection.cursor() as cursor:
                sql = """INSERT INTO course (name, start_date, end_date, id_teacher)
                         VALUES (%S, %s, %s, %s)"""
                cursor.execute(sql, (course.name, course.start_date, course.end_date, course.teacher.id))
                course_id = cursor.lastrowid

                # Insérer les relations avec étudiants
                for student in course.students_taking_it:
                    sql_takes = "INSERT INTO takes (student_nbr, id_course) VALUES (%s, %s)"
                    cursor.execute(sql_takes, (student.student_nbr, course_id))

                Dao.connection.commit()
                course.id = course_id
                return course_id
        except Exception as e:
            print(f"Erreur lors de la création du cours : {e}")
            Dao.connection.rollback()
            return 0


    def read(self, id_course: int) -> Optional[Course]:
        """Renvoit le cours correspondant à l'entité dont l'id est id_course
           (ou None s'il n'a pu être trouvé)"""
        #course: Optional[Course]
        
        with Dao.connection.cursor() as cursor:
            sql = "SELECT * FROM course WHERE id_course=%s"
            cursor.execute(sql, (id_course,))
            record = cursor.fetchone()

        if not record :
            return None

        # Créer l'objet cours
        course = Course(
            name=record['name'],
            start_date=record['start_date'],
            end_date=record['end_date']
        )
        course.id = record['id_course']

        # Charger l'enseignant
        teacher_dao = TeacherDao()
        course.teacher = teacher_dao.read(record['id_teacher'])

        # Charger les étudiants qui suivent ce cours
        with Dao.connection.cursor() as cursor:
            sql = """SELECT s.student_nbr
                     FROM takes t
                     JOIN student s ON t.student_nbr = s.student_nbr
                     WHERE t.id_course = %s"""
            cursor.execute(sql, (id_course,))
            student_records = cursor.fetchall()

        student_dao = StudentDao()
        for student_record in student_records:
            student = student_dao.read(student_record['student_nbr'])
            if student:
                course.students_taking_it.append(student)
                student.courses_taken.append(course)

        return course

    def read_all(self) -> List[Course]:
        with Dao.connection.cursor() as cursor:
            sql = "SELECT id_course FROM course ORDER BY start_date"
            cursor.execute(sql)
            records = cursor.fetchall()

        courses = []
        for record in records:
            course = self.read(record['id_course'])
            if course:
                courses.append(course)

        return courses

    def update(self, obj: Course) -> bool:
        return False

    def delete(self, obj: Course) -> bool:
        return False



