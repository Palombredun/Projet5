#!/usr/bin/env python3


# Project for the start-up Pur Beurre.

import json

from app import choice
from app import databasemanager as dbm
from app import printing


print("\n\nBienvenue sur l'application de Pur Beurre")
print("Vous pourrez ici choisir des aliments plus sains\n\
et consulter ceux que vous avez déjà remplacés.\n")

is_good = 1
# Instanciation of the classes :
choice = choice.Choice(4)


loop = True

while loop:
    print("\n1 - Choisissez un aliment à remplacer")
    print("2 - Consulter les aliments précédemments remplacés")
    print("Pour quitter, tapez Q.")
    userChoice = input()

    if userChoice.lower() == 'q':
        break
    try:
        userChoice = int(userChoice)
        if userChoice not in (1,2):
            print("Entrez 1 ou 2")
    except:
        print("Veuillez entrer un choix valide.")

    if userChoice == 1:
        
        # Categories' choices : 
        choice.chooseCategory()

        # choose food :
        idReplacedProduct = choice.chooseFood(choice.categoryName)

        # choose substitute or not :
        choice.chooseSubstitute(idReplacedProduct)