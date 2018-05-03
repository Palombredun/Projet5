#!/usr/bin/env python3

class Print():
    def __init__(self):
        self.a = 'toto'

    def printList(self,list_):
        """
        This function takes a list and prints properly. If there are more
        than 20 elements it creates pages in order to have a more elegant presentation.
        """
        print("\n")
        for i, elt in enumerate(list_):
            print("{} - {}".format(i, list_[i]))        
        print("\n")
    
    def printListOfDict(self, listDict_, detail=False):
        """
        This function takes a list of dictionnaries and prints it.
        If the parameter detail is set to False, it only prints the index 
        and the product name.
        On the contrary, if detail is set to True, the function prints
        all the keys and values in the list.
        """
        if detail is False:
            #if there are 20 or less elements in the list :
            if len(listDict_) < 21:
                for i in range(len(listDict_)):
                    print(i, " - ", listDict_[i]['product_name'])
            
            else:
                page_number = 1 + len(listDict_)//20
                page_counter = 1
                # print the 20 first products :
                for i in range(20):
                    print("{} - {}".format(i, listDict_[i]['product_name']))
                print("Page 1/{}".format(page_number))
                keep_loop_going = 1
                
                while keep_loop_going:
                    print("Pour passer à la page suivante, tapez S,")
                    user_input = input("une fois que vous avez fait votre choix, tapez Q\n")
                    if user_input.lower() == 's':
                        print("Page {}/{}".format(page_counter+1, page_number))
                        if page_counter < page_number-1:
                            for i in range(20*page_counter, 20*page_counter + 20):
                                print("{} - {}".format(i, listDict_[i]['product_name']))
                        else:
                            for i in range(page_counter*20, len(listDict_)):
                                print("{} - {}".format(i, listDict_[i]['product_name']))
                            break
                        page_counter += 1
                    if user_input.lower() == 'q':
                        break
        else:
            # The format of this printing is a bit bifferent : on a line
            # is printed the key and on the line below the value.
            # for the ingredients (which we know are separated by a comma),
            # we do a carriage return for more clarity.
            if type(listDict_) is dict():
                elements = listDict_[0]
            else:
                elements = listDict_
                
            print("Nom du produit : ", elements['product_name'])
            print("Code : ", elements['id_product'])
            print("Score nutritionnel : ", elements['nutritional_score'])
            print("Page de l'aliment : ",elements['url'])
            print("Lieu d'achat : ", elements['purchase_place'])
            print("Ingrédients : ")
            for elt in elements['ingredients'].split(','):
                print("\t",elt)
            print("\n\n")

    
    def printJSON(self, datasFile):
        """
        Prints the name of the product replaced and its substitute
        """
        print("Aliment  -  Substitut")
        print("____________________________\n")
        i = 0
        for elt in datasFile["Produits"]:
            print(elt["product_remplace"], " - ", elt["nom_produit"])
