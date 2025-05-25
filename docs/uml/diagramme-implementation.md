# Diagramme d'implémentation

# Structure du Laboratoire 1

app/
├── console.py
├── models.py
└── persistance/
    └── db.py

# Couches Logiciels

1. Couche Présentation:
app/console.py
Interface console et menus

2. Couche Logique Métier:
app/models.py
Règles de gestion des stocks

3. Couche Persistance:
app/persistance/db.py
Configuration SQLAlchemy
Session de base de données

# Dépendances

console.py → models.py → db.py
- Console utilise les modèles
- Modèles utilisent la session DB

# Technologies d'Implémentation

- Langage: Python 3.11
- ORM: SQLAlchemy 2.0+
- Base de données: SQLite
- Tests: pytest
- Qualité: pylint
- Déploiement: Docker
