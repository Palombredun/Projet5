#!/usr/bin/env python3

import json, requests

class Interactions:
    def __init__(self, loopNumber):
        self.category_name = ""
        self.loopNumber = loopNumber

    def getCategory(self, category_name):
        """
        Interacts with the API to get the categories.
        First we print the 20 biggest categories, among which the user has to choose.
        Thanks to requests, we get the page of this category. We then extract the 
        subcategories and again ask to make a choice. The user has to take a total
        of 
        """
        # creation of the link
        link = "https://fr.openfoodfacts.org/categorie/" + category_name.replace(" ", "-")
        # request :
        r = requests.get(link)
        # extraction of the categories in a category :
        text = r.text.split('\n')
        list_category = []
        categoryMarkerFront = "<li><a href=\"/categorie/"
        categoryMarkerBack = "\" class=\"tag well_known"
        for line in text:
            if categoryMarkerFront in line and categoryMarkerBack in line:
                list_category.append(line)

        # if the list is empty (no subcategory), we move on to the next step
        if len(list_category) == 0:
            return 0, list_category
        tmp = 0
        for line in list_category:
            # cleans the list from the html tags
            catMFSize = len(categoryMarkerFront)
            catMBSize = line.find(categoryMarkerBack)
            line = line[catMFSize:catMBSize:]
            line = line.replace("-", " ")
            list_category[tmp] = line
            tmp+=1
        return 1, list_category

    def getJSON(self, category_name):
        """
        Gets all the products from the last category chosen and puts them in
        a list, at 1 page of products per index of the list.
        """
        # request on the last category to get the json (at least the first page)
        link = "https://fr.openfoodfacts.org/categorie/" +\
            category_name.replace(" ", "-") + ".json"
        r = requests.get(link)
        # Search of the number of pages (in order to get them all (and in the darkness bind them))
        count = "count"
        tmp=[]
        list_json = []
        list_json.append(r.content)
        data = json.loads(r.text)
        s = data['count']
        request_number = s//20 + 1
        # get the other pages of products
        if s > 20:
            for i in range(2, request_number+1):
                link = "https://fr.openfoodfacts.org/categorie/" +\
                    category_name.replace(" ", "-") + "/" +\
                    str(request_number) + ".json"
                r = requests.get(link)
                list_json.append(r.content)
        # returns a list containing the json with the products (20 json per page)
        return list_json