# LOG430 - labo 1: Architecture Client-Serveur 2-Tiers

Ce laboratoire met en œuvre une architecture client-serveur à deux tiers en Python. Il propose une application console permettant à un employé du magasin de gérer les produits, enregistrer des ventes, gérer les retours, et consulter l’état du stock via une base de données persistante (SQLite) à travers SQLAlchemy.

## Fonctionnalités de l'application console

- Ajouter un produit
- Afficher les produits avec alerte de stock
- Rechercher un produit (par ID ou nom)
- Enregistrer une vente (avec gestion des transactions et mise à jour du stock)
- Gérer les retours (annulation de vente avec restauration du stock)
- Vérifier la cohérence des stocks automatiquement

## Architecture

- **Client**: Application console Python
- **Serveur**: Base de données SQLite (persistence locale simulant le serveur)
- **ORM**: SQLAlchemy
- **Tests et Qualité**: Pytest, Pylint
- **CI/CD**: GitHub Actions

## Structure du laboratoire

├── app/
│ ├── console.py # Interface console principale
│ ├── models.py # Modèles ORM (Produit, Vente, LigneVente)
│ └── persistance/
│ └── db.py # Connexion à la BD et session
├── tests/ # Tests unitaires
├── .github/workflows/ # Pipeline CI GitHub Actions
└── README.md

## Prérequis

- Git
- Docker et Docker Compose
- Python 3.11 ou supérieur

## Technologies utilisées

- Python 3.11
- Pytest
- Pylint
- Docker
- GitHub Actions
- Docker Hub

## Choix techniques

- __Python 3.11__: Choisi pour sa stabilité et son développement rapide d'applications
- __Pytest__: Sélectionné pour sa simplicité d'utilisation
- __Pylint__: Utilisé pour maintenir un code propre et conforme aux standards de Python
- __Docker__: Implémenté pour assurer la portabilité de l'environnement de développement
- __GitHub Actions__: Choisi pour son intégration native avec GitHub et sa facilité de configuration
- __Docker Hub__: Utilisé comme registre public pour stocker l'image Docker

## Image Docker

L’image Docker est automatiquement construite et poussée sur Docker Hub à chaque mise à jour de la branche `main`.

__Lien Docker Hub :__  
[`aicha0000/log430-lab1`](https://hub.docker.com/repository/docker/aicha0000/log430-lab1)

## Développement local: Configuration de l'environnement

1. Cloner le dépôt:
git clone <https://github.com/Aicha0000/log430-lab0.git>
cd log430-lab0
2. Créer et activer un environnement virtuel:
python -m venv venv
source venv/bin/activate
3. Installer les dépendances
pip install -r requirements.txt

## Fichier `requirements.txt`

Le fichier contient les dépendances suivantes utilisées dans le projet :
greenlet==3.2.2
SQLAlchemy==2.0.41
typing_extensions==4.13.2
pytest==7.4.0
pylint==3.0.0

## Exécution des Tests

pytest

## Exécution du Linter

pylint app/ tests/

## Exécution de Docker

docker run aicha0000/log430-lab1

## Pipeline CI/CD

Ce laboratoire utilise Github Actions pour l'intégration et la livraison continues:
À chaque push sur le main ou pull request:

- le code est récupéré
- L'environnement Python est configuré
- Les dépendances sont installées
- Les vérifications de linting sont exécutées
- Les tests unitaires sont exécutés
- L'image Docker est construite et poussée vers Docker Hub (uniquement sur la branche main)

## Auteur

Aicha Aanounou
