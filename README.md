# LOG430 - Lab 2: Architecture Multi-Magasins avec Repository Pattern

## Démarrage rapide

```bash
# Démarrer l'application
docker run -d --name lab2-postgres -e POSTGRES_DB=lab2_db -e POSTGRES_USER=lab2_user -e POSTGRES_PASSWORD=lab2_password -p 5432:5432 postgres:15
docker run -d --name lab2-app --link lab2-postgres:postgres -p 8000:8000 -e DATABASE_URL="postgresql://lab2_user:lab2_password@postgres:5432/lab2_db" aicha0000/log430-lab2:latest

# Vérifier le fonctionnement
curl http://localhost:8000/health
open http://localhost:8000/web

# Exécuter les tests
docker exec lab2-app python3 -m pytest tests/ -v
```

## Description

Système de gestion pour 5 magasins avec centre logistique et maison mère. Evolution du Lab 1 vers une architecture utilisant le pattern Repository avec PostgreSQL.

## Fonctionnalités

- UC1: Rapports consolidés des ventes
- UC2: Consultation stock central et réapprovisionnement
- UC3: Tableau de bord des performances
- UC4: Mise à jour des produits
- UC6: Traitement des demandes de réapprovisionnement
- UC7: Alertes automatiques via webhooks
- UC8: Interface web avec API REST

## Architecture

- Interface: Consoles utilisateur spécialisées
- Service: Couche logique métier
- Repository: Abstraction d'accès aux données
- Database: PostgreSQL
- API: FastAPI

## Structure

```
lab2/
├── prototype/
│   ├── commun/
│   │   ├── modeles/
│   │   └── repositories/
│   └── services/
│       ├── administration/
│       ├── logistique/
│       └── magasin/
├── production/
├── tests/
├── docs/
└── sql/
```

## Prérequis

- Docker et Docker Compose
- Python 3.11

## Technologies

- Python 3.11
- FastAPI
- PostgreSQL
- Docker

## Installation locale

```bash
git clone https://github.com/Aicha0000/log430-lab0.git
cd log430-lab0/lab2
docker-compose up
```

## Interfaces

### Interface web
- API: http://localhost:8000
- Dashboard: http://localhost:8000/web
- Documentation: http://localhost:8000/docs

### Interfaces console

```bash
# Interface employé magasin
docker-compose exec api python3 -c "
import sys; sys.path.append('/app/prototype')
from services.magasin.interface_console import main
main()"

# Interface gestionnaire 
docker-compose exec api python3 -c "
import sys; sys.path.append('/app/prototype')
from services.administration.interface_gestionnaire import main
main()"

# Interface centre logistique
docker-compose exec api python3 -c "
import sys; sys.path.append('/app/prototype')
from services.logistique.main import main
main()"
```

## Tests

```bash
# Tous les tests
docker-compose exec api python3 -m pytest tests/ -v

# Tests par catégorie
docker-compose exec api python3 -m pytest tests/test_unitaires.py -v
docker-compose exec api python3 -m pytest tests/test_integration.py -v  
docker-compose exec api python3 -m pytest tests/test_e2e.py -v
```

## Configuration base de données

PostgreSQL avec variables d'environnement:
```
DB_HOST=postgres
DB_PORT=5432
DB_NAME=lab2_db
DB_USER=lab2_user
DB_PASSWORD=lab2_password
```

## API principales

- GET /api/consolide - Rapport consolidé
- GET /api/central - Stock central
- GET /api/dashboard - Tableau de bord
- PUT /api/produits/{id} - Modification produit
- GET /api/alertes/faible-stock - Alertes stock

## Documentation

- Architecture: docs/rapport-arc42.md
- Décisions: docs/adr/
- Diagrammes: docs/uml/

## Auteur

Aicha Aanounou
