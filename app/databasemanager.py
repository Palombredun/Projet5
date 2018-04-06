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
                                    id_substitute BIGINT UNSIGNED PRIMARY KEY,
                                    id_product BIGINT UNSIGNED NOT NULL)
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
    
    def executeSQL(self, sql, addProducts=False, compareProducts=False, addSubstitute=False, \
                    findProduct=False, listProducts=None, tupleCompareProduct=None, \
                    tupleSubstitue=None, prodToFind=None):
        
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
                    # Get all the elements from listProducts :
                    for content in listProducts:
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
                            category_name = data['products'][j]['categories']
                            category_name = unicodedata.normalize('NFKD', category_name).\
                                                           encode('ascii', 'ignore').decode()
                            purchase_place = data['products'][j]['purchase_places']
                            j += 1
                            # Put the values in a tuple :
                            tupledValues = (index, product_name, nutritional_score, product_url, \
                                    ingredients_text, purchase_place)                                
                            cursor.execute(self.sql, tupledValues)
                            connection.commit()
                            result = cursor.fetchall()
                            return result
                
                elif compareProducts:
                    cursor.execute(sql, tupleCompareProduct)
                    connection.commit()
                    result = cursor.fetchall()
                    return result
                
                elif addSubstitute:
                    cursor.execute(sql, tupleSubstitue)
                    connection.commit()

                elif findProduct:
                    findProduct = (findProduct,)
                    cursor.execute(sql, findProduct)
                    connection.commit()
                    result = cursor.fetchall()
                    return result
        
        finally:
            connection.close()