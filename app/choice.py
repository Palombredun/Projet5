#!/usr/bin/env python3

import json
import requests
import unicodedata

from app import printing
from app import databasemanager

class Choice:
    def __init__(self):
        self.urlCategory = ""
        self.URL = "https://fr.openfoodfacts.org/"
        self.categoryName = ""
        self.userChoice = ""

        self.printer = printing.Print()
        self.dbm = databasemanager.DataBaseManager()
   

    def chooseCategory(self):
        # get the categories from the API :
        listCategoriesNames = self.getCategory()

        # Print them and ask the user to choose one
        self.printer.printList(listCategoriesNames)
        self.userChoice = input("Veuillez choisir une catégorie : ")
        try:
            self.userChoice = int(self.userChoice)
            if self.userChoice in range(len(listCategoriesNames)):
                pass
        except:
            print("Veuillez entrer un numéro valide")

        # Update categoryName :
        self.categoryName = listCategoriesNames[self.userChoice]

        return self.categoryName


    def getCategory(self):
        """
        create a link pointing to the categories of the OpenFoodFacts as JSON file
        and download it in order to extract the 20 first categories (less the 2 firsts)
        and return them as a list.
        """
        # Create the link
        link = self.URL + "categories.json"
        
        # Make the request :
        r = requests.get(link)
        self.categories = json.loads(r.text)
        
        # Create the list of categories :
        listCategoriesNames = []  
        i = 0
        while i <= 21:
            listCategoriesNames.append(self.categories['tags'][i]['name'])
            listCategoriesNames[i] = unicodedata.normalize('NFKD', listCategoriesNames[i]).\
                            encode('ascii', 'ignore').decode()
            i+= 1
        listCategoriesNames = listCategoriesNames[2:]

        return listCategoriesNames


    def chooseFood(self, categoryName):
        """
        Function called when the user has to chose a product 
        to replace from the last category chosen.
        """

        # Check if the category chosen by the user is in the database :
        self.dbm.sql = "SELECT * FROM `Products` WHERE `category_name` = %s"
        result = self.dbm.executeSQL(self.dbm.sql, findCategory=True, categoryToFind=self.categoryName)

        # Else, get the products whith the module requests and load it in the table :
        if len(result) == 0:
            listJSON = self.getProducts(categoryName)
            self.dbm.sql = "INSERT INTO `Products` \
                    (`id_product`, `product_name`, `nutritional_score`, \
                    `url`, `ingredients`, `category_name`, `purchase_place`) \
                    VALUES (%s, %s, %s, %s, %s, %s, %s)"
            self.dbm.executeSQL(self.dbm.sql, addProducts=True, listProducts=(listJSON, self.categoryName))
            self.dbm.sql = "SELECT * FROM `Products` WHERE `category_name` = %s"
            result = self.dbm.executeSQL(self.dbm.sql, findCategory=True, categoryToFind=self.categoryName)

        # Ask the user a product to choose :
        while True:
            print("\n\nVoici les aliments appartenant à la catégorie", \
                "que vous avez sélectionnée :", sep="\n")
            self.printer.printListOfDict(result)
            self.userChoice = input("Entrez le numéro de l'aliment que vous souhaitez remplacer : ")
            try:
                self.userChoice = int(self.userChoice)
                if self.userChoice <= len(result):
                    break
            except:
                print("Veuillez entrer un numéro valide")

        idReplacedProduct = result[self.userChoice]['id_product']

        # Verify that this product hasn't already been replaced :
        self.dbm.sql = "SELECT * FROM `Products` WHERE `id_product` = %s"
        result = self.dbm.executeSQL(self.dbm.sql, findCategory=True, categoryToFind=idReplacedProduct)
        if len(result) == 0:
            print("Vous avez déjà cherché un substitut pour cet aliment.")
            return 1
        return idReplacedProduct


    def getProducts(self, categoryName):
        """
        Gets all the products from the last category chosen and puts them in
        a list, at 1 page of products per index of the list.
        """
        # request on the last category to get the json (at least the first page)
        link = "https://fr.openfoodfacts.org/categorie/" +\
            categoryName.replace(" ", "-") + ".json"
        r = requests.get(link)
        listJSON =[r.content]

        # returns a list containing the json with the products (20 json per page)
        return listJSON


    def chooseSubstitute(self, idReplacedProduct):
        """
        Ask the user to choose a substitute among the products with a better
        nutritional score than the one he has chosen.
        """

        # Get the nutritional score of the product chosen :
        self.dbm.sql = "SELECT `nutritional_score` FROM `Products` WHERE `id_product`=%s"
        result = self.dbm.executeSQL(self.dbm.sql, findCategory=True, categoryToFind=idReplacedProduct)
        nutritionalScore = result[0]['nutritional_score']


        # Find all products within the category with a better nutritional score
        self.dbm.sql = " SELECT * FROM `Products` WHERE `nutritional_score`>%s and `category_name`=%s "
        tmp = (nutritionalScore, self.categoryName)
        result = self.dbm.executeSQL(self.dbm.sql, compareProducts=True, \
                                     tupleCompareProduct=tmp)
          
        # Find the product with the best nutritional score :
        idSubstitute = 0
        for product in result:
            if nutritionalScore < product['nutritional_score']:
                nutritionalScore = product['nutritional_score']
                idSubstitute = product['id_product']

        # If no other product is healthier, back to the menu :
        if idSubstitute == 0:
            print("\nAucun aliment de cette catégorie n'est meilleur",\
                "pour la santé que celui que vous avez sélectionné.", sep="\n")
            return

        # Else, print the details of the potential substitute and propose the user to save it :
        else:
            # Get all caracteristics of the product :
            self.dbm.sql = "SELECT * FROM `Products` WHERE `id_product`=%s"
            result = self.dbm.executeSQL(self.dbm.sql, findCategory=True, categoryToFind=idSubstitute)
            print("\nVoilà l'aliment avec le meilleur score nutritionnel :\n")
            # Print these caracteristics :
            self.printer.printListOfDict(result, detail=1)
            
            # Ask the user to remember this substitute or not :
            while True:
                self.userChoice = input("Pour sauvegarder ce substitut, tapez Y, sinon N : ")                
                # If the user choses not to save the substitute, back to menu
                if self.userChoice.lower() == 'n':
                    return
                elif self.userChoice.lower() == 'y':
                    # Add the substitute to the table Substitute :
                    self.dbm.sql = "INSERT INTO `Substitute` (`id_product`, `id_substitute`) \
                                    VALUES (%s, %s)"

                    values = (idReplacedProduct, idSubstitute)
                    print(values)
                    self.dbm.executeSQL(self.dbm.sql, addSubstitute=True, tupleSubstitute=values)
                    return
                else:
                    print("Entrez une réponse valide")
    

    def getDetails(self):
        """
        Print the substitutes chosen by the user, and offer him to print the details
        of these products (or quit)
        """
        self.userChoice = ""
        while self.userChoice != 'q':
            # print subtitutes :
            self.dbm.sql = "SELECT * FROM Products INNER JOIN Substitute ON Products.id_product=Substitute.id_substitute"    
            result = self.dbm.executeSQL(self.dbm.sql, getSubstitutes=True)
            self.printer.printListOfDict(result)

            # ask the user to make a choice :
            print("Pour afficher les détails d'un produit, entrez son numéro, sinon tapez Q pour quitter")
            self.userChoice = input("Votre choix : ")
            if self.userChoice.lower() == 'q':
                return

            try:
                self.userChoice = int(self.userChoice)
                print(self.userChoice)
                if self.userChoice <= len(result):
                    pass
            except:
                print("Entrez un choix valide")

            # get the id of the product
            productToPrint = result[self.userChoice]
            self.printer.printListOfDict(productToPrint, detail=1)