### Projet pour la start-up Pur Beurre

Ce projet est développé dans le cadre de la formation Openclassrooms "Développeur d'application Python". Il a pour but de se familiariser avec l'utilisation d'API REST et MySQL. L'API utilisée dans ce projet est celle du site Open Food Facts qui compile des aliments et leurs propriétés nutritionnelles.


#### Fonctionnalités :

###### Prérequis
Le programme fonctionne avec Python3 et MySQL pour les requêtes. Il n'y a pas besoin d'installer l'API d'Open Food Facts pour fonctionner. Il faut cependant installer les bibliothèques indiquées dans le fichier requirements.txt avec la commande pip install > requirements.txt ainsi que MySQL.

###### Utilisation : 

Au lancement du programme, deux choix s'offrent à l'utilisateur :
1. Choix 1 :
Choisir un aliment à substituer
2. Choix 2 :
Consulter les aliments substitués

Si l'utilisateur choisit la première catégorie, le programme lui pose les questions suivantes :
* Sélectionner la catégorie
* Sélectionner l'aliment
* Le programme propose un substitut, sa description, un magasin où l'acheteret un lien vers la page Open Food Facts concernant cet aliment
* Enregistrer le résultat dans la base de données.

Si l'utilisateur choisit la seconde catégorie, on le renvoit vers la base de données contenant les aliments qu'il a remplacés.


#### Licence :
Ce projet est sous la licence GPL, voir le fichier LICENCE.md pour les détails.
De par sa nature pédagogique, ce projet n'a cependant pas vocation à être reproduit.

Auteur : Baptiste Fina