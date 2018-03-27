#!/usr/bin/env python3

import json, requests, unicodedata
from app import printing

class Choice:
    def __init__(self, loopNumber):
        self.loopNumber = loopNumber
        self.loopCounter = 0
        self.urlCategory = ""
        self.URL = "https://fr.openfoodfacts.org/"
        self.categoryName = ""
        self.userChoice = ""


    def chooseCategory(self):
        # get the categories
        listCategories = self.getCategory(self.categoryName)
        
        #print them and ask the user to choose one
        printing.printCategories(listCategories)
        userChoice = input("Veuillez choisir une catégorie : ")
        try:
            userChoice = int(userChoice)
            if userChoice in range(1,21):
                pass
        except:
            print("Veuillez entrer un numéro valide")
        
        self.categoryName = listCategories[userChoice]
        self.categoryName = unicodedata.normalize('NFKD', self.categoryName).\
                                        encode('ascii', 'ignore').decode()

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
                            self.categoryName.replace('', '-') + \
                            "/categories.json"
        # Make request :
        r = requests.get(link)
        self.categories = r.json
        listCategories = []
        
        # get the 21 firsts categories (or less) :
        i=0
        while (i < 21) or (i < self.categories['count']):
            listCategories.append(self.categories['tags'][i]['name'])            
            if self.categoryName == "":
                # the first category name is the current one, so useless
                del listCategories[21]
            else:
                #else, delete the last one
                del listCategories[0]
        return listCategories

    
    def chooseFood(self, categoryName):
        listJSON = self.getProducts(categoryName)
        # load products into table Products
        # use executeSQL(sql) in order
        # printing.printList(resultList)
    

    def chooseSubstitute(self):
        pass
    

    def getProducts(self, categoryName):
        """
        Gets all the products from the last category chosen and puts them in
        a list, at 1 page of products per index of the list.
        """
        # request on the last category to get the json (at least the first page)
        link = "https://fr.openfoodfacts.org/categorie/" +\
            categoryName.replace(" ", "-") + ".json"
        r = requests.get(link)
        # Search of the number of pages (in order to get them all (and in the darkness bind them))
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