# ADR-002: Kong API Gateway

## Status
Accepted

## Context
Les 8 microservices ont besoin d'un point d'entree unique pour la gestion du trafic. Il faut choisir entre Kong, Nginx, ou Traefik.

## Decision
On utilise Kong comme API Gateway avec sa propre base PostgreSQL.

## Rationale
- Gateway specialise pour microservices
- Routage dynamique par service configuré
- Interface admin sur port 8002
- Support PostgreSQL pour persistence config
- Plugins disponibles pour monitoring

## Consequences
- Point d'entree unique sur port 8000
- Routes configurees: /api/products, /api/customers, /api/orders, etc.
- Kong admin API sur port 8002
- Kong database separee des services
- Latence variable observee (36-344ms selon service)
- Single point of failure sans cluster
- Configuration manuelle des routes necessaire