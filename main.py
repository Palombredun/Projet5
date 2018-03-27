#!/usr/bin/env python3


# Project for the start-up Pur Beurre.

import json
from app import choice
from app import databasemanager
from app import printing


print("\n\nBienvenue sur l'application de Pur Beurre")
print("Vous pourrez ici choisir des aliments plus sains\n\
et consulter ceux que vous avez déjà remplacés.\n")

is_good = 1
# Instanciation of the classes :
category = interactions.Interactions(3)
printing = printing.Print()



while is_good:
    dbm = databasemanager.DataBaseManager()
    print("1 - Quel aliment souhaitez-vous remplacer ?")
    print("2 - Retrouver mes aliments substitués")
    print("Tapez Q pour quitter.")

    userChoice = input()
    if userChoice.lower() == "q":
        break
    try:
        userChoice = int(userChoice)
    except:
        print("Entrez 1 ou 2 pour faire votre choix.")


    if userChoice == 1:
        # Begin by printing the 20 biggest categories :
        printing.printList(cst.CATEGORIES)
        # The user chooses the category of the products he wants to change :
        categoryNumber = printing.chooseCategory()
        categoryName = cst.CATEGORIES[categoryNumber]


        # The user chooses up to 3 times a subcategory :
        for i in range(category.loopNumber):
            # Get the subcategories :
            listCategories = []
            returnCode, listCategories = category.getCategory(categoryName)
            # If there is no subcategory : 
            if returnCode == 0:
                break
            # Print the subcategories :
            printing.printList(listCategories)
            # Choose the subcategory :
            categoryNumber = printing.chooseCategory()
            categoryName = listCategories[categoryNumber]


        # Get the products from the last category chosen by the user :
        listJSON = category.getProducts(categoryName)
        # Insert these products into the database
        dbm.sql = "INSERT INTO `Aliments` \
            (`id_produit`, `nom_produit`, `score_nutritionnel`, \
            `url`, `ingredients`, `lieu_achat`) \
            VALUES (%s, %s, %s, %s, %s, %s)"
        resultList = dbm.executeSQL(dbm.sql, listJSON)
        # Print all the products from the last category chosen
        dbm.sql = "SELECT * FROM `Aliments`"
        print("\n\n")
        resultList = dbm.executeSQL(dbm.sql)
        print("Voici les aliments appartenant à la catégorie que vous avez sélectionné :")
        printing.printListOfDict(resultList)


        # The user now chooses the product to replace :
        idReplacedProduct = input("\nEntrez le numéro du produit que vous souhaitez remplacer : ")            
        try:
            idReplacedProduct = int(idReplacedProduct)
        except:
            print("Entrez un numéro valide")
        replacedProduct = resultList[idReplacedProduct]['nom_produit'] # this will be useful later


        # Select all products with a better nutritional score :
        dbm.sql = "SELECT * FROM `Aliments` WHERE `score_nutritionnel` > %s"
        resultList = dbm.executeSQL(dbm.sql, idReplacedProduct)

        # Several possibilities :
        # No substitute :
        if len(resultList) == 0:
            print("\nAucun aliment de cette catégorie n'est meilleur",\
                "pour la santé que celui que vous avez sélectionné.", sep="\n")
            break
        # Only 1 substitute :
        elif len(resultList) == 1:
            print("\nIl n'y a qu'un seul aliment meilleur pour",\
                "la santé que celui que vous avez sélectionné :", sep="\n")
            printing.printListOfDict(resultList)
        # Several substitutes :
        elif len(resultList) > 1:
            print("\nVoici les aliments meilleurs pour la santé",\
                "que celui que vous avez sélectionné :", sep="\n")
            printing.printListOfDict(resultList)


        # Ask the user to chose a substitute (if he wants one) :
        print("Si vous souhaitez sauvegardez un substitut, entrez son numéro.")
        inpt = input("Sinon, tapez N : ")
        if inpt.lower() == 'n':
            break
        else:
            try:
                idSubstitute = int(inpt)
            except:
                print("Entrez un numéro valide :")
            # Create a dictionary containing the caracteristics of the product chosen by the user
            dictSubstitute = resultList[idSubstitute]
            print("\n\nVoici les détails du substitut que vous avez choisi : ")
            printing.printListOfDict(dictSubstitute, detail=1)
            # Add a column so the user knows what the substitute replaces
            dictSubstitute["product_remplace"] = replacedProduct
            # Open the file datas.json which contains the previous substitutes
            with open('substitutes.json', 'a') as f1:
                with open('substitutes.json', 'r') as f2:
                    try:
                        datas = json.load(f2)
                    except:
                        datas={}
                        datas["Produits"] = []
                    with open('substitutes.json', 'w') as f3:
                        datas["Produits"].append(dictSubstitute)
                        json.dump(datas, f3, indent=4)
    

    elif userChoice == 2:
        with open("substitutes.json", "r") as f:
            datas = json.load(f)
            print("Voici les produits que vous avez choisi de remplacer, avec leur substitut : ")
            printing.printJSON(datas)


loop = 1

while loop:
    print("\n1 - Choisissez un aliment à remplacer")
    print("2 - Consulter les aliments précédemments remplacés")
    print("Enfin, tapez Q pour quitter.")

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
        choice.loopCounter = 0
        while choice.loopCounter < choice.loopNumber:
            choice.chooseCategory()
            choice.loopCounter += 1
        
        choice.chooseFood(choice.categoryName)