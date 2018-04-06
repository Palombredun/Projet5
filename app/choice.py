#!/usr/bin/env python3

import json, requests, unicodedata
from app import printing
from app import databasemanager

class Choice:
    def __init__(self, loopNumber):
        self.loopNumber = loopNumber
        self.loopCounter = 0
        self.urlCategory = ""
        self.URL = "https://fr.openfoodfacts.org/"
        self.categoryName = ""
        self.userChoice = ""

        self.printer = printing.Print()
        self.dbm = databasemanager.DataBaseManager()
   

    def chooseCategory(self):
        # get the categories from the API :
        listCategoriesNames = self.getCategory(self.categoryName)

        # Print them and ask the user to choose one
        self.printer.printList(listCategoriesNames)
        self.userChoice = input("\nVeuillez choisir une catégorie : ")
        try:
            self.userChoice = int(self.userChoice)
            if self.userChoice in range(len(listCategoriesNames)):
                pass
        except:
            print("Veuillez entrer un numéro valide")

        # Update categoryName :
        self.categoryName = listCategoriesNames[self.userChoice]
        self.categoryName = unicodedata.normalize('NFKD', self.categoryName).\
                                        encode('ascii', 'ignore').decode()

        return self.categoryName


    def getCategory(self, categoryName=""):
        """
        Creates a link with the category name, if it is empty, simply gets
        the top 20 categories.
        Once the link is created, use the lib request to get the json file containing the
        (sub)categories. The function also returns 0 if the category does not contain
        subcategories, thus passing to the next step of the code.
        """
        # Create link :
        if self.categoryName == "":
            link = self.URL + "categories.json"
        else:
            link = self.URL + "categorie/" + \
                            self.categoryName.replace(' ', '-') + \
                            "/categories.json"
        
        # Make the request :
        r = requests.get(link)
        self.categories = json.loads(r.text)
               
        # Append list listCategoriesName containing the 60 categories :
        i = 0
        listCategoriesNames = []
        while i < self.categories['count']:
            listCategoriesNames.append(self.categories['tags'][i]['name'])
            listCategoriesNames[i] = unicodedata.normalize('NFKD', listCategoriesNames[i]).\
                                encode('ascii', 'ignore').decode()
            i += 1
        
        # If there are more than 60 categories, delete the rest :
        if len(listCategoriesNames) > 60:
            del listCategoriesNames[60:]
            # the first category name is the last one chosen, so useless
            del listCategoriesNames[0]

        return listCategoriesNames

    
    def getProducts(self, categoryName):
        """
        Gets all the products from the last category chosen and puts them in
        a list, at 1 page of products per index of the list.
        """
        # request on the last category to get the json (at least the first page)
        link = "https://fr.openfoodfacts.org/categorie/" +\
            categoryName.replace(" ", "-") + ".json"
        r = requests.get(link)
        # Search the number of pages (in order to get them all (and in the darkness bind them))
        count = "count"
        tmp=[]
        listJSON = []
        listJSON.append(r.content)
        data = json.loads(r.text)
        s = data['count']
        request_number = s//20 + 1
        # get the other pages of products
        if s > 20:
            for i in range(2, request_number+1):
                link = "https://fr.openfoodfacts.org/categorie/" +\
                    categoryName.replace(" ", "-") + "/" +\
                    str(request_number) + ".json"
                r = requests.get(link)
                listJSON.append(r.content)
        # returns a list containing the json with the products (20 json per page)
        return listJSON


    def chooseFood(self, categoryName):
        """
        Function called when the user has to chose a product 
        to replace from the last category chosen.
        """

        # Check if the category chosen by the user is in the database :
        self.dbm.sql = "SELECT `category_name` \
                        FROM `Products` WHERE `category_name` = %s"
        result = self.dbm.executeSQL(self.dbm.sql, findProduct=True, prodToFind=self.categoryName)
        
        # If the category is in the Table Products, get the products :
        if len(result) != 0:  
            self.dbm.sql = "SELECT * FROM `Products` WHERE `category_name` = %s"
            result = self.dbm.executeSQL(self.dbm.sql, findProduct=True, prodToFind=self.categoryName)
        
        # Else, get the products whith the module requests and load it in the table :
        else:
            listJSON = self.getProducts(categoryName)
            self.dbm.sql = "INSERT INTO `Products` \
                    (`id_product`, `product_name`, `nutritional_score`, \
                    `url`, `ingredients`, `category_name`, `purchase_place`) \
                    VALUES (%s, %s, %s, %s, %s, %s, %s)"
            result = self.dbm.executeSQL(self.dbm.sql, addProducts=True, listProducts=listJSON)

        print("\n\nVoici les aliments que vous avez sélectionné :")
        self.printer.printListOfDict(result)
        self.userChoice = input("Entrez le numéro de l'aliment que vous souhaitez remplacer : ")
        try:
            self.userChoice = int(self.userChoice)
            if self.userChoice <= len(result):
                pass
        except:
            print("Veuillez entrer un numéro valide")

        idReplacedProduct = result[self.userChoice]['score']
        return idReplacedProduct


    def chooseSubstitute(self, idReplacedProduct):
        """
        Ask the user to choose a substitute among the products with a better
        nutritional score than the one he has chosen.
        """
        self.dbm.sql = "SELECT * WHERE `nutritional_score` > %s and `category_name` = %s"
        result = self.dbm.executeSQL(self.dbm.sql, compareProduct=True, \
                                    tupleCompareProduct=(idReplacedProduct,self.categoryName))
        
        # Print the result :
        if len(result) == 0:
            print("\nAucun aliment de cette catégorie n'est meilleur",\
                "pour la santé que celui que vous avez sélectionné.", sep="\n")
            return
        # Only 1 substitute :
        elif len(result) == 1:
            print("\nIl n'y a qu'un seul aliment meilleur pour",\
                "la santé que celui que vous avez sélectionné :", sep="\n")
            printer.printListOfDict(result)
        # Several substitutes :
        elif len(result) > 1:
            print("\nVoici les aliments meilleurs pour la santé",\
                "que celui que vous avez sélectionné :", sep="\n")
            printer.printListOfDict(result)

        # Ask the user to chose a substitute (if he wants one) :
        print("Si vous souhaitez sauvegardez un substitut, entrez son numéro.")
        self.userChoice = input("Sinon, tapez N : ")
        
        if self.userChoice.lower() == 'n':
            return
        else:
            try:
                idSubstitute = int(self.userChoice)
                idSubstitute = result[idSubstitute]['score']
            except:
                print("Entrez un numéro valide :")
        # Add of the substitute to the table Substitute :
        self.dbm.sql = "INSERT INTO `Substitute` (`id_product`, `id_substitute` \
                        VALUES (%s, %s)"
        values = (idReplacedProduct, idSubstitute)
        self.dbm.executeSQL(self.dbm.sql, addSubstitute=True, tupleSubstitute=values)

        # Print the details of the product chosen by the user
        self.dbm.sql = "SELECT * FROM `Products` \
                        INNER JOIN `Substitute` \
                            ON `Products.id_product` = `Substitute.id_substitute` \
                        WHERE `Products.id_product` = %s"
        self.dbm.executeSQL(self.dbm.sql, findProduct=True, prodToFind=idReplacedProduct)
        print("\n\nVoici les détails du substitut que vous avez choisi : ")
        printing.printListOfDict(dictSubstitute, detail=1)
    
    
    