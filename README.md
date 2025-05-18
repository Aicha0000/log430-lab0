# LOG430 - labo 0: Pipeline CI avec Docker et Github Actions

Ce laboratoire est une application minimaliste en Python avec deux tests unitaires, une analyse de code et une conteneurisation Docker. Il inclut un pipeline CI/CD complet utilisant GitHub Actions qui exécute des tests, valide la qualité du code, et construit et pousse une image Docker vers Docker Hub.

## Structure du laboratoire

.
├── .github/workflows   # Définitions des workflows GitHub Actions
│   ├── main.yml        # Pipeline CI principal
│   └── ci.yml          # Configurations CI supplémentaires
├── app/                # Le Code source
│   ├── __init__.py
│   └── main.py         # Module principal de l'application
├── tests/              # Suite de tests
│   ├── __init__.py
│   └── test_unitaire.py # Tests unitaires
├── docker-compose.yml  # Configuration Docker Compose
├── .dockerignore       # Fichiers à exclure du contexte Docker
├── .gitignore          # Fichiers à exclure de Git
├── Dockerfile          # Définition de l'image Docker
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
[`aicha0000/log430-lab0`](https://hub.docker.com/repository/docker/aicha0000/log430-lab0)

## Développement local: Configuration de l'environnement

1. Cloner le dépôt:
git clone <https://github.com/Aicha0000/log430-lab0.git>
cd log430-lab0
2. Créer et activer un environnement virtuel:
python -m venv venv
source venv/bin/activate
3. Installer les dépendances
pip install -r requirements.txt

## Exécution des Tests

pytest

## Exécution du Linter

pylint app/ tests/

## Exécution de Docker

docker run aicha0000/log430-lab0

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
