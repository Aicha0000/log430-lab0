# Diagramme d'implémentation
```` mermaid 
graph TB
    subgraph "Structure du Laboratoire 1"
        subgraph "app/"
            Console[console.py<br/>Interface console et menus]
            Models[models.py<br/>Règles de gestion des stocks]
            
            subgraph "persistance/"
                DB[db.py<br/>Configuration SQLAlchemy<br/>Session de base de données]
            end
        end
    end
    
    subgraph "Couches Logicielles"
        subgraph "Couche Présentation"
            CP[app/console.py]
        end
        
        subgraph "Couche Logique Métier" 
            CLM[app/models.py]
        end
        
        subgraph "Couche Persistance"
            CPers[app/persistance/db.py]
        end
    end
    
    subgraph "Technologies"
        Python[Python 3.11]
        SQLAlchemy[SQLAlchemy 2.0+]
        SQLite[SQLite]
        Pytest[pytest]
        Pylint[pylint]
        Docker[Docker]
    end
    
    %% Dépendances:
    Console --> Models
    Models --> DB
    
    %% Relations avec les couches:
    CP -.-> Console
    CLM -.-> Models
    CPers -.-> DB
    
    %% Technologies utilisées:
    Console -.-> Python
    Models -.-> SQLAlchemy
    DB -.-> SQLite
    Python -.-> Docker
 ```` 
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
