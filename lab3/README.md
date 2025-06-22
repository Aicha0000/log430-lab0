# Lab 3 - API RESTful Multi-Magasins

## Structure Minimale
```
lab3/
└── README.md          # Documentation Lab 3
```

## Authentification
Token statique: `lab3-static-token`

Usage:
```bash
curl -H "Authorization: Bearer lab3-static-token" http://localhost:8000/api/central
```

## Documentation API
Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc

## Endpoints Principaux
- GET /api/consolide - UC1 Rapports consolidés
- GET /api/central - UC2 Stock central  
- GET /api/dashboard - UC3 Tableau de bord
- PUT /api/produits/{id} - UC4 Mise à jour produits
- GET /api/alertes/faible-stock - UC7 Alertes stock
- GET /web - UC8 Interface web

## Tests
```bash
docker-compose exec api python -m pytest tests/ -v
```