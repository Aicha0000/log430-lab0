# ADR-003: Stack Observabilite

## Status
Accepted

## Context
Les 8 microservices necessitent un monitoring distribue pour tracer les performances et erreurs. Il faut choisir la stack d'observabilite.

## Decision
Stack Prometheus + Grafana pour le monitoring des microservices et databases.

## Rationale
- Prometheus pour collecter metriques de tous les services
- Grafana pour dashboards consolides
- Metriques standardisees avec prometheus_client
- Monitoring des 8 PostgreSQL databases
- Vue d'ensemble sur architecture distribuee

## Consequences
- Endpoint /metrics sur chaque des 8 services
- Prometheus sur port 9091
- Grafana sur port 3001 (admin/admin)
- Metriques observees: latence 1.53ms moyenne, 12.63% taux erreur
- Monitoring Kong Gateway inclus
- Dashboards pour analyser performance vs architecture precedente
- Retention limitee des donnees historiques