# -*- coding: utf-8 -*-

"""
Classe Dao[Teacher]
"""

from models.teacher import Teacher
from daos.dao import Dao
from daos.address_dao import AddressDao
from dataclasses import dataclass
from typing import Optional, List


@dataclass
class TeacherDao(Dao[Teacher]):
    def create(self, teacher: Teacher) -> int:
        """Crée en BD l'entité Teacher correspondant à l'enseignant teacher

        :param teacher: à créer sous forme d'entité Teacher en BD
        :return: l'id de l'entité insérée en BD (0 si la création a échoué)
        """
        try:
            with Dao.connection.cursor() as cursor:
                # D'abord créer la personne dans la table person
                sql_person = """INSERT INTO person (first_name, last_name, age, id_address)
                                VALUES (%s, %s, %s, %s)"""
                address_id = teacher.address.id if teacher.address else None
                cursor.execute(sql_person, (teacher.first_name, teacher.last_name,
                                          teacher.age, address_id))
                person_id = cursor.lastrowid

                # Puis créer l'enseignant dans la table teacher
                sql_teacher = "INSERT INTO teacher (hiring_date, id_person) VALUES (%s, %s)"
                cursor.execute(sql_teacher, (teacher.hiring_date, person_id))
                teacher_id = cursor.lastrowid
                Dao.connection.commit()

                teacher.id = teacher_id
                return teacher_id
        except Exception as e:
            print(f"Erreur lors de la création de l'enseignant : {e}")
            Dao.connection.rollback()
            return 0

    def read(self, id_teacher: int) -> Optional[Teacher]:
        """Renvoit l'enseignant correspondant à l'entité dont l'id est id_teacher
           (ou None s'il n'a pu être trouvé)"""
        #teacher: Optional[Teacher] = None

        with Dao.connection.cursor() as cursor:
            sql = """SELECT t.id_teacher, t.hiring_date, p.id_person, p.first_name,
                            p.last_name, p.age, p.id_address, a.street, a.city, a.postal_code
                     FROM teacher t
                     JOIN person p ON t.id_person = p.id_person
                     LEFT JOIN address a ON p.id_address = a.id_address
                     WHERE t.id_teacher = %s"""
            cursor.execute(sql, (id_teacher,))
            record = cursor.fetchone()

        if record:
            return self._record_to_teacher(record)
        return None

    def read_all(self) -> List[Teacher]:
        """Renvoit tous les enseignants de la base de données"""
        #teachers = []

        with Dao.connection.cursor() as cursor:
            sql = """SELECT t.id_teacher, t.hiring_date, p.id_person, p.first_name,
                            p.last_name, p.age, p.id_address, a.street, a.city, a.postal_code
                     FROM teacher t
                     JOIN person p ON t.id_person = p.id_person
                     LEFT JOIN address a ON p.id_address = a.id_address"""
            cursor.execute(sql)
            records = cursor.fetchall()

        return [self._record_to_teacher(record) for record in records]

    def update(self, obj: Teacher) -> bool:
        return False

    def delete(self, obj: Teacher) -> bool:
        return False

    def _record_to_teacher(self, record: dict) -> Teacher:

        # Créer l'adresse si elle existe
        address = None
        if record.get('id_address'):
            address = Address(
                street=record['street'],
                city=record['city'],
                postal_code=record['postal_code']
            )
            address.id = record['id_address']

        # Créer l'enseignant
        teacher = Teacher(
            first_name=record['first_name'],
            last_name=record['last_name'],
            age=record['age'],
            hiring_date=record['hiring_date']
        )
        teacher.id = record['id_teacher']
        teacher.address = address

        return teacher




