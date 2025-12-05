# -*- coding: utf-8 -*-

"""
Classe Dao[Student]
"""

from ecole.models.student import Student
from models.person import Person
from ecole.daos.dao import Dao
from daos.address_dao import AddressDao
from ecole.models.address import Address
from dataclasses import dataclass
from typing import Optional, List


@dataclass
class StudentDao(Dao[Student]):
    def create(self, student: Student) -> int:
        """Crée en BD l'entité Student correspondant à l'élève student

        :param student: à créer sous forme d'entité Student en BD
        :return: l'id de l'entité insérée en BD (0 si la création a échoué)
        """
        try:
            with Dao.connection.cursor() as cursor:
                # D'abord créer la personne dans la table person
                sql_person = """INSERT INTO person (first_name, last_name, age, id_address)
                                VALUES (%s, %s, %s, %s)"""
                address_id = student.address.id if student.address else None
                cursor.execute(sql_person, (student.first_name, student.last_name,
                                          student.age, address_id))
                person_id = cursor.lastrowid

                # Puis créer l'étudiant dans la table student
                sql_student = "INSERT INTO student (student_nbr, id_person) VALUES (%s, %s)"
                cursor.execute(sql_student, (student.student_nbr, person_id))
                Dao.connection.commit()

                # Mettre à jour le compteur statique
                if student.student_nbr > Student.students_nb:
                    Student.students_nb = student.student_nbr

                return student.student_nbr
        except Exception as e:
            print(f"Erreur lors de la création de l'étudiant : {e}")
            Dao.connection.rollback()
            return 0

    def read(self, student_nbr: int) -> Optional[Student]:
        """Renvoit l'élève correspondant à l'entité dont le numéro est student_nbr
           (ou None s'il n'a pu être trouvé)"""
        #student: Optional[Student] = None

        with Dao.connection.cursor() as cursor:
            sql = """SELECT s.student_nbr, p.id_person, p.first_name, p.last_name,
                            p.age, p.id_address, a.street, a.city, a.postal_code
                     FROM student s
                     JOIN person p ON s.id_person = p.id_person
                     LEFT JOIN address a ON p.id_address = a.id_address
                     WHERE s.student_nbr = %s"""
            cursor.execute(sql, (student_nbr,))
            record = cursor.fetchone()

        if record:
            return self._record_to_student(record)
        return None

    def read_all(self) -> List[Student]:
        """Renvoit tous les étudiants de la base de données"""
        #students = []

        with Dao.connection.cursor() as cursor:
            sql = """SELECT s.student_nbr, p.id_person, p.first_name, p.last_name,
                            p.age, p.id_address, a.street, a.city, a.postal_code
                     FROM student s
                     JOIN person p ON s.id_person = p.id_person
                     LEFT JOIN address a ON p.id_address = a.id_address"""
            cursor.execute(sql)
            records = cursor.fetchall()

        student = []
        for record in records:
            student.append(self._record_to_student(record))

        # Mettre à jour le compteur statique
        if student:
            Student.students_nb = max(s.student_nbr for s in student)

        return student

    def update(self, obj: Student) -> bool:
        return False

    def delete(self, obj: Student) -> bool:
        return False

    def _record_to_student(self, record: dict) -> Student:
        """Convertit un record SQL en objet Student"""
        # Créer l'adresse si elle existe
        address = None
        if record.get('id_address'):
            address = Address(
                street=record['street'],
                city=record['city'],
                postal_code=record['postal_code']
            )
            address.id = record['id_address']

            # Créer l'étudiant
        student = Student(
            first_name=record['first_name'],
            last_name=record['last_name'],
            age=record['age']
        )
        student.student_nbr = record['student_nbr']
        student.address = address

        return student
