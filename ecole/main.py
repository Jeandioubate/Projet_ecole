#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Application de gestion d'une école - Version simplifiée
Chargement et affichage uniquement
"""
# initialisation d'un ensemble de cours, enseignants et élèves composant l'école
# school.init_static()

from business.school import School

def main():
    print("ÉCOLE - CHARGEMENT DES DONNÉES")
    print("=" * 50)

    # Créer l'école (charge automatiquement toutes les données)
    school = School()

    # Afficher les statistiques
    school.display_stats()

    # Afficher toutes les données
    school.display_all_data()

if __name__ == '__main__':
    main()





