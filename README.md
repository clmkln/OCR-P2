# OCR-P2

**Utilisez les bases de Python pour l'analyse de marché**


## Description

Extraction des informations des produits du site http://books.toscrape.com/

- product_page_url
- universal_ product_code (upc)
- title
- price_including_tax
- price_excluding_tax
- number_available
- product_description
- category
- review_rating
- image_url


## Cas d'usage

**A.** Récupérer les données d'un seul livre à partir de son URL

**B.** Récupérer les informations des livres d'une certaine catégortie à partir de son URL

**C.** Récupérer l'ensembles des données des livres, toutes catégories confondues.


## Données

Les données extraites seront stockées dans le répertoire courant d'exécution du script.


## Installation

- Cloner le repository actuel et naviguer dans le répertoire :
```
git clone https://github.com/clmkln/OCR-P2.git
```
- Installer les prérequis :
```
make all
```
- Utiliser la commande suivante afin d'activer l'environnement virtuel :
```
source venv/bin/activate
```

Si vous souhaitez nettoyer le projet des données générées :
```
make clean
```

 ## Utilisation

```
python scrap-book.py
```