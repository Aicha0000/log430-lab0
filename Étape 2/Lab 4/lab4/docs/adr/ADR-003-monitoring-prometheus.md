# ADR-003: Monitoring avec Prometheus et Grafana

## Status
Accepted

## Context
Le lab demande l'observabilite avec les 4 Golden Signals. Il faut choisir entre Prometheus+Grafana ou autres solutions.

## Decision
Stack Prometheus + Grafana pour le monitoring.

## Rationale
- Prometheus pour collecter les metriques
- Grafana pour visualiser les dashboards
- Standards de l'industrie
- Facile a integrer avec FastAPI
- Dashboards preconfigures disponibles

## Consequences
- Metrics endpoint /metrics sur l'API
- Dashboards pour latence, trafic, erreurs, saturation
- Retention des donnees limitee
- Overhead minimal sur l'API
- Bon pour identifier les bottlenecks