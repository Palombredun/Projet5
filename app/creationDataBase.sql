
CREATE TABLE Products(
                    id_product BIGINT UNSIGNED PRIMARY KEY,
                    product_name VARCHAR(80) NOT NULL,
                    nutritional_score SMALLINT NOT NULL,
                    url VARCHAR(200) NOT NULL,
                    ingredients TEXT NOT NULL,
                    category_name TEXT NOT NULL,
                    purchase_place VARCHAR(100))


CREATE TABLE Substitute(
                        id_substitute BIGINT UNSIGNED PRIMARY KEY,
                        id_product BIGINT UNSIGNED NOT NULL)
                        ENGINE=INNODB;

ALTER TABLE `Substitute`
                ADD CONSTRAINT `fk_id_substitute` FOREIGN KEY (`id_substitute`)
                REFERENCES `Products`(`id_product`)
                
ALTER TABLE `Substitute`
                ADD CONSTRAINT `fk_id_product` FOREIGN KEY (`id_product`)
                REFERENCES `Products`(`id_product`)
     