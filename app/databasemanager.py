#!/usr/bin/env python3

import json
import pymysql.cursors
import unicodedata

class DataBaseManager:
    def __init__(self):
        self.sql = ""
        connection = pymysql.connect(host='localhost', 
                                    user='root', 
                                    password='123', 
                                    charset='utf8',
                                    cursorclass=pymysql.cursors.DictCursor)
        try:
            # Creation of the Database
            with connection.cursor() as cursor:
                cursor.execute("""DROP DATABASE IF EXISTS PurBeurre""")
                connection.commit()
                cursor.execute("""CREATE DATABASE IF NOT EXISTS PurBeurre""")
                connection.commit()
                cursor.execute("""USE PurBeurre""")
                connection.commit()
            # Creation of the Tables
                cursor.execute("""CREATE TABLE IF NOT EXISTS Aliments(
                                id_produit INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
                                nom_produit VARCHAR(80),
                                score_nutritionnel SMALLINT NOT NULL,
                                url VARCHAR(200) NOT NULL,
                                ingredients TEXT NOT NULL,
                                lieu_achat VARCHAR(100))
                                ENGINE=INNODB;
                                """)
                connection.commit()
        finally:
                connection.close()
    def executeSQL(self, sql, *params):
        self.sql = sql
        connection = pymysql.connect(host='localhost', 
                                    user='root', 
                                    password='123', 
                                    charset='utf8',
                                    cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                cursor.execute("""USE PurBeurre""")
                connection.commit()
                # if there is no parameter, simply execute the sql command and return the result :
                if len(list(params)) == 0:
                    cursor.execute(self.sql)
                    connection.commit()
                    result = cursor.fetchall()
                # in case of a parameter (add products to a table) :
                else:
                    # if the parameter is a list, it means we want to add products to the table
                    if type(params[0]) is list:
                        list_json = params[0]
                        # Get all the elements from list_json
                        index = 0
                        for content in list_json:
                            data = json.loads(content)
                            j = 0
                            # For each page, we iterate on the number of products to add them to the table
                            while j < len(data['products']):
                                product_name = data['products'][j]['product_name']
                                nutritional_score = data['products'][j]['nutrition_score_debug']
                                nutritional_score = nutritional_score[-2:]
                                try:
                                    nutritional_score = int(nutritional_score)
                                except:
                                    nutritional_score = -100
                                product_url = data['products'][j]['url']
                                ingredients_text = data['products'][j]['ingredients_text_debug']
                                ingredients_text = unicodedata.normalize('NFKD', ingredients_text).\
                                                               encode('ascii', 'ignore').decode()
                                purchase_place = data['products'][j]['purchase_places']
                                j += 1
                                index += 1
                                tupledValues = (index, product_name, \
                                        nutritional_score, product_url, \
                                        ingredients_text, purchase_place)                                
                                cursor.execute(self.sql, tupledValues)
                                connection.commit()
                    # if the parameter is an int, we want to select products with a better
                    # nutritional score
                    elif type(params[0]) is int:
                        tupledValues = (params[0],)
                        cursor.execute(self.sql, tupledValues)
                        connection.commit()
                    result = cursor.fetchall()
        finally:
            connection.close()
        return result

    def dropDatabase(self):
        connection = pymysql.connect(host='localhost', 
                                    user='root', 
                                    password='123', 
                                    charset='utf8',
                                    cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                cursor.execute("""DROP DATABASE IF EXISTS PurBeurre""")
                connection.commit()
        finally:
            connection.close()