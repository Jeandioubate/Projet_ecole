# -*- coding: utf-8 -*-

"""
Classe Dao[Address]
"""

from models.address import Address
from daos.dao import Dao
from dataclasses import dataclass
from typing import Optional, List


@dataclass
class AddressDao(Dao[Address]):
    def create(self, address: Address) -> int:
        """Crée en BD l'entité Address correspondant à l'adresse address

        :param address: à créer sous forme d'entité Address en BD
        :return: l'id de l'entité insérée en BD (0 si la création a échoué)
        """
        try:
            with Dao.connection.cursor() as cursor:
                sql = "INSERT INTO address (street, city, postal_code) VALUES (%s, %s, %s)"
                cursor.execute(sql, (address.street, address.city, address.postal_code))
                Dao.connection.commit()
                address.id = cursor.lastrowid
                return address.id
        except Exception as e:
            print(f"Erreur lors de la création de l'adresse : {e}")
            Dao.connection.rollback()
            return 0

    def read(self, id_address: int) -> Optional[Address]:
        """Renvoit l'adresse correspondant à l'entité dont l'id est id_address
           (ou None s'il n'a pu être trouvé)"""
        address: Optional[Address] = None

        with Dao.connection.cursor() as cursor:
            sql = "SELECT * FROM address WHERE id_address = %s"
            cursor.execute(sql, (id_address,))
            record = cursor.fetchone()

        if record is not None:
            address = Address(
                street=record['street'],
                city=record['city'],
                postal_code=record['postal_code']
            )
            address.id = record['id_address']
            return address

        return None

    def read_all(self) -> List[Address]:
        """Renvoit toutes les adresses de la base de données"""

        with Dao.connection.cursor() as cursor:
            sql = "SELECT * FROM address"
            cursor.execute(sql)
            records = cursor.fetchall()

        addresses = []
        for record in records:
            address = Address(
                street=record['street'],
                city=record['city'],
                postal_code=record['postal_code']
            )
            address.id = record['id_address']
            addresses.append(address)

        return addresses

    def update(self, obj: Address) -> bool:
        return False

    def delete(self, obj: Address) -> bool:
        return False