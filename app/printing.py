#!/usr/bin/env python3

class Print():
    def __init__(self):
        pass

    def printList(self,list_):
        """
        This function takes a list and prints properly. If there are more
        than 20 elements it creates pages in order to have a more elegant presentation.
        """
        # if there is 20 or less elements in the list, simply prints them :
        if len(list_) == 0:
            print("Il n'y a aucun produit répertorié dans cette catégorie.")
        elif len(list_) < 21:
            for i, elt in enumerate(list_):
                print("{} - {}".format(i, list_[i]))
        # Else, we begin by printing the 20 first elements of the list :
        else:
            # count the number of page :
            page_number = 1 + len(list_)//20
            page_counter = 1
            for i in range(20):
                print("{} - {}".format(i, list_[i]))
            print("Page 1/{}".format(page_number))
            keep_loop_going = 1
            while keep_loop_going:
                # the user can print the next (or previous page) or pass to the next step
                print("Pour passer à la page suivante, tapez S,")
                user_input = input("une fois que vous avez fait votre choix tapez Q\n") 
                if user_input.lower() is 's':
                    print("Page {}/{}".format(page_counter+1, page_number))
                    if page_counter < page_number-1:
                        # if we're not at the last page :
                        for i in range(20*page_counter, 20*page_counter + 20):
                            print("{} - {}".format(i, list_[i]))
                    else:
                        # if it is the last page :
                        for i in range(page_counter*20, len(list_)):
                            print("{} - {}".format(i, list_[i]))
                        break
                    page_counter += 1
                if user_input.lower() == 'q':
                    break
    def printCategories(self, listCategories):
        """Prints a list of categories"""
        for i in range(len(listCategories)):
            print(i, ' - ', listCategories)
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
                    print(i, " - ", listDict_[i]['nom_produit'])
            
            else:
                page_number = 1 + len(listDict_)//20
                page_counter = 1
                # print the 20 first products :
                for i in range(20):
                    print("{} - {}".format(i, listDict_[i]['nom_produit']))
                print("Page 1/{}".format(page_number))
                keep_loop_going = 1
                
                while keep_loop_going:
                    print("Pour passer à la page suivante, tapez S,")
                    user_input = input("une fois que vous avez fait votre choix, tapez Q\n")
                    if user_input.lower() == 's':
                        print("Page {}/{}".format(page_counter+1, page_number))
                        if page_counter < page_number-1:
                            for i in range(20*page_counter, 20*page_counter + 20):
                                print("{} - {}".format(i, listDict_[i]['nom_produit']))
                        else:
                            for i in range(page_counter*20, len(listDict_)):
                                print("{} - {}".format(i, listDict_[i]['nom_produit']))
                            break
                        page_counter += 1
                    if user_input.lower() == 'q':
                        break
        

        else:
            # The format of this printing is a bit bifferent : on a line
            # is printed the key and on the line below the value.
            # for the ingredients (which we know are separated by a comma),
            # we do a carriage return for more clarity.
            for key in listDict_.keys():
                if key != "ingredients_text":
                    print(key, " : ")
                    print("\t", listDict_[key])
                else:
                    print(key, " :")
                    listedIngredients = listDict_[key].split(',')
                    if len(listDict_[key]) > 5:
                        for key in listDict_.keys():
                            print("\t",listDict_[key])
                    else:
                        while i < listDict_[key]:
                            for j in range(5):
                                print("\t", elt, ", ")
    def printJSON(self, datasFile):
        """
        Prints the name of the product replaced and its substitute
        """
        print("Aliment  -  Substitut")
        print("____________________________\n")
        i = 0
        for elt in datasFile["Produits"]:
            print(elt["product_remplace"], " - ", elt["nom_produit"])
