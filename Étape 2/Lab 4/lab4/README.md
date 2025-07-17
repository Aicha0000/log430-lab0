# Lab 4 - Observabilite, Load Balancing et Cache

## Vue d'ensemble

Ce lab introduit des pratiques avancees d'observabilite, de test de charge, de load balancing et d'optimisation des performances via le caching pour le systeme multi-magasins.

## Architecture

Le lab se decompose en 3 etapes sequentielles:

1. **Observabilite**: Monitoring avec Prometheus/Grafana et 4 Golden Signals
2. **Load Balancing**: NGINX avec multiple instances API et tolerance aux pannes  
3. **Cache**: Redis distribue pour optimiser les performances

## Structure

```
lab4/
├── monitoring/          # Etape 1 - Observabilite
├── load-balancer/       # Etape 2 - Load Balancer
├── cache/              # Etape 3 - Cache Redis
├── load-tests/         # Scripts de test k6
└── docs/               # Documentation ADR et UML
```

## Resultats Performance

| Etape | RPS | Latence P95 | Taux Erreur | Amelioration |
|-------|-----|-------------|-------------|-------------|
| Baseline | 20 req/s | 80ms | 12% | - |
| Load Balancer | 38.46 req/s | 41.23ms | 7.67% | +92% RPS |
| Cache Redis | 86.48 req/s | 31.38ms | 4.89% | +124% RPS |

## Technologies

- **Monitoring**: Prometheus, Grafana
- **Load Balancer**: NGINX
- **Cache**: Redis
- **Tests**: k6
- **Infrastructure**: Docker Compose