# Lab 3 - API Multi-Magasins

## Setup rapide

```bash
cd "Lab 3"
docker-compose up -d
```

## Tests

```bash
# Setup environment first
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run les tests
python lab3/test_lab3.py
```

## Structure project

```
Lab 3/
├── production/main.py          # App FastAPI principal  
├── lab3/
│   ├── test_lab3.py           # Tests auto
│   ├── test_pytest.py         # Tests pour CI/CD
│   └── postman-collection.json # Collection API
├── docker-compose.yml         # Config Docker
└── requirements.txt           # Dependencies Python
```

## API Usage

**Token requis**: `lab3-static-token`

```bash
curl -H "Authorization: Bearer lab3-static-token" \
     http://localhost:8000/api/central
```

## Endpoints disponibles

- `GET /api/consolide` - UC1: Rapports consolidated  
- `GET /api/central` - UC2: Stock central
- `GET /api/dashboard` - UC3: Performance dashboard
- `PUT /api/produits/{id}` - UC4: Update produits
- `GET /api/alertes/faible-stock` - UC7: Stock alerts
- `GET /web` - Interface web

## Documentation

- Swagger: http://localhost:8000/docs
- Health: http://localhost:8000/health