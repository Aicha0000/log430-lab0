# ADR-004: Database per Service Pattern

## Status
Accepted

## Context
L'architecture microservices demande une isolation des donnees entre services. Il faut choisir entre database partagee ou database per service.

## Decision
On implemente le pattern "database per service" avec PostgreSQL dedie pour chaque microservice.

## Rationale
- Isolation complete des donnees
- Pas de coupling entre services via database
- Chaque service peut evoluer son schema independamment
- Resilience: panne d'une DB n'affecte qu'un service
- Scalabilite independante des donnees

## Consequences
- 7 PostgreSQL containers avec volumes persistants
- Configuration DATABASE_URL specifique par service
- Shared database utilities dans /shared/database.py
- Startup time augmente (attente databases ready)
- Latence accrue vs stockage memoire (12-15ms vs <5ms)
- Cart service: 3 instances partagent cart-db
- Complexite operationnelle avec 7 bases a maintenir
- Backup et monitoring necessaires pour chaque DB

## Services et Databases
- products-service → products-db
- inventory-service → inventory-db  
- reports-service → reports-db
- sales-service → sales-db
- customers-service → customers-db
- orders-service → orders-db
- cart-service (x3) → cart-db (partagée)
- checkout-service → checkout-db