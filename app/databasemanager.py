#!/usr/bin/env python3

import json
import pymysql.cursors
import unicodedata

class DataBaseManager:
    def __init__(self):
        self.sql = ""

        # Get password:
        with open('mdp.txt', 'r') as file:
            mdp = file.read()
        mdp=mdp[:3]

        connection = pymysql.connect(host='localhost', 
                                    user='root', 
                                    password=mdp, 
                                    charset='utf8',
                                    cursorclass=pymysql.cursors.DictCursor)
        try:
            # Creation of the Database
            with connection.cursor() as cursor:
                #cursor.execute("""DROP DATABASE IF EXISTS PurBeurre""")
                #connection.commit()
                sql = "SHOW DATABASES LIKE 'PurBeurre'"
                cursor.execute(sql)
                connection.commit()
                result = cursor.fetchone()

                if result is None:
                    # Create database PurBeurre :
                    cursor.execute("""CREATE DATABASE IF NOT EXISTS PurBeurre;""")
                    connection.commit()
                    cursor.execute("""USE PurBeurre""")
                    connection.commit()
                    # Creation of the Tables
                    cursor.execute("""CREATE TABLE Products(
                                    id_product BIGINT UNSIGNED PRIMARY KEY,
                                    product_name VARCHAR(80) NOT NULL,
                                    nutritional_score SMALLINT NOT NULL,
                                    url VARCHAR(200) NOT NULL,
                                    ingredients TEXT NOT NULL,
                                    category_name TEXT NOT NULL,
                                    purchase_place VARCHAR(100))
                                    ENGINE=INNODB;
                                    """)
                    connection.commit()

                    cursor.execute("""CREATE TABLE Substitute(
                                    id_substitute BIGINT UNSIGNED NOT NULL,
                                    id_product BIGINT UNSIGNED PRIMARY KEY)
                                    ENGINE=INNODB;
                                    """)
                    connection.commit()
                    cursor.execute("""ALTER TABLE `Substitute`
                                    ADD CONSTRAINT `fk_id_substitute` FOREIGN KEY (`id_substitute`)
                                    REFERENCES `Products`(`id_product`)
                                    """)
                    connection.commit()
                    cursor.execute("""ALTER TABLE `Substitute`
                                    ADD CONSTRAINT `fk_id_product` FOREIGN KEY (`id_product`)
                                    REFERENCES `Products`(`id_product`)
                                    """)
                    connection.commit()                               
        finally:
                connection.close()
    
    def executeSQL(self, sql, addProducts=False, listProducts=None, \
                              compareProducts=False, tupleCompareProduct=None, \
                              addSubstitute=False, tupleSubstitute=None, \
                              findCategory=False, categoryToFind=None,
                              getSubstitutes=False):
        
        connection = pymysql.connect(host='localhost', 
                                    user='root', 
                                    password='123', 
                                    charset='utf8',
                                    cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                cursor.execute("""USE PurBeurre""")
                connection.commit()
                
                if addProducts:
                    listJSON = listProducts[0]
                    categoryName = listProducts[1]
                    # Get all the elements from listJSON :
                    for content in listJSON:
                        data = json.loads(content)
                        j = 0

                        # For each page, iterate on the number of products to add them to the table
                        while j < len(data['products']):
                            index = data['products'][j]['code']
                            product_name = data['products'][j]['product_name']
                            nutritional_score = data['products'][j]['nutrition_score_debug']
                            nutritional_score = nutritional_score[-2:]
                            # If the nutritional score is missing, it takes the value -100
                            try:
                                nutritional_score = int(nutritional_score)
                            except:
                                nutritional_score = -100
                            product_url = data['products'][j]['url']
                            ingredients_text = data['products'][j]['ingredients_text_debug']
                            ingredients_text = unicodedata.normalize('NFKD', ingredients_text).\
                                                           encode('ascii', 'ignore').decode()
                            category_name = categoryName
                            try:
                                purchase_place = data['products'][j]['purchase_places']
                            except:
                                purchase_place = ""
                            j += 1
                            # Put the values in a tuple :
                            tupledValues = (index, product_name, nutritional_score, product_url, \
                                    ingredients_text, category_name, purchase_place)                                
                            cursor.execute(sql, tupledValues)
                            connection.commit()
                
                elif compareProducts:
                    cursor.execute(sql, tupleCompareProduct)
                    connection.commit()
                    result = cursor.fetchall()
                    return result
                
                elif addSubstitute:
                    cursor.execute(sql, tupleSubstitute)
                    connection.commit()

                elif findCategory:
                    cursor.execute(sql, categoryToFind)
                    connection.commit()
                    result = cursor.fetchall()
                    return result

                elif getSubstitutes:
                    cursor.execute(sql)
                    connection.commit()
                    result = cursor.fetchall()
                    return result
        
        finally:
            connection.close()