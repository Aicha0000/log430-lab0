# Lab 5 - Architecture Microservices avec API Gateway

## Vue d'ensemble

Ce lab fait evoluer le systeme multi-magasins vers une architecture microservices complete avec API Gateway, load balancing et observabilite distribuee.

## Architecture

L'architecture se decompose en 8 microservices independants:

1. **Services Magasin**: products, inventory, sales, reports
2. **Services E-commerce**: customers, orders, cart (3 instances), checkout
3. **API Gateway**: Kong avec load balancing et routage
4. **Observabilite**: Prometheus/Grafana distribue

## Structure

```
lab5/
├── microservices/       # 8 services independants
│   ├── products-service/
│   ├── inventory-service/
│   ├── sales-service/
│   ├── reports-service/
│   ├── customer-service/
│   ├── order-service/
│   ├── cart-service/    # 3 instances load-balancees
│   └── checkout-service/
├── monitoring/          # Stack Prometheus/Grafana
├── tests/              # Scripts k6 pour microservices
├── setup-kong*.sh      # Configuration Kong Gateway
└── docs/               # Rapport Arc42 et ADR
```

## Demarrage rapide

```bash
# Lancement de tous les services
docker-compose up -d

# Configuration Kong Gateway
./setup-kong.sh
./setup-kong-cors.sh
./setup-kong-loadbalancing.sh

# Verification des services
curl http://localhost:8000/api/products
curl http://localhost:8000/api/cart
```

## Endpoints API Gateway

| Service | Endpoint | Port Direct | Instances |
|---------|----------|-------------|-----------|
| Products | /api/products | 8002 | 1 |
| Inventory | /api/inventory | 8003 | 1 |
| Sales | /api/sales | 8004 | 1 |
| Reports | /api/reports | 8005 | 1 |
| Customers | /api/customers | 8006 | 1 |
| Orders | /api/orders | 8007 | 1 |
| Cart | /api/cart | 8008 | 3 (load-balanced) |
| Checkout | /api/checkout | 8009 | 1 |

**API Gateway**: http://localhost:8000 (Kong)  
**Admin Kong**: http://localhost:8001

## Monitoring

**Prometheus**: http://localhost:8010/targets  
**Grafana**: http://localhost:8011 (admin/admin)

Chaque microservice expose ses metriques sur `/metrics`

## Tests de charge

```bash
# Test via API Gateway
k6 run tests/k6-test.js

# Test direct vs Gateway
k6 run load_test.js
```

## Resultats Performance

| Approche | Latence Moyenne | Overhead | Load Balancing |
|----------|----------------|----------|----------------|
| Direct | 5.47ms | - | - |
| Via Gateway | 21.12ms | +15.65ms | Round-robin |
| Premiere requete | 88ms vs 7ms | +81ms | Initialisation |

## Technologies

- **Microservices**: FastAPI, PostgreSQL
- **API Gateway**: Kong
- **Load Balancing**: Kong Upstream (cart-service)
- **Monitoring**: Prometheus, Grafana  
- **Tests**: k6, JMeter
- **Infrastructure**: Docker Compose (23 conteneurs)