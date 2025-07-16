# ADR-001: Architecture Microservices

## Status
Accepted

## Context
Le systeme multi-magasins de vente de boissons evolue vers e-commerce. Lab 4 avait 3 domaines monolithiques: administration, logistique, magasin. Pour Lab 5, on doit extraire services existants et ajouter capacites e-commerce.

## Decision
Architecture microservices avec 8 services: 4 extraits de Lab 4 + 4 nouveaux pour e-commerce.

**Domaines Lab 4 extraits:**
- products-service: catalogue boissons (admin)
- inventory-service: gestion stock (logistique) 
- reports-service: rapports business (admin)
- sales-service: ventes magasin (magasin)

**Nouveaux services e-commerce:**
- customers-service: comptes clients
- order-service: gestion commandes
- cart-service: panier achat
- checkout-service: validation commande

## Rationale
- Respecte decomposition domaines Lab 4
- Separation magasin physique vs e-commerce
- Services partages: inventory entre magasin et web
- Scalabilite independante par service
- Database per service pour isolation

## Consequences
- 8 microservices avec PostgreSQL dedicacees
- Kong Gateway pour routing unifie
- Load balancing sur cart-service (3 instances)
- CORS configure pour web clients
- Monitoring Prometheus/Grafana maintenu
- Complexite operationnelle: 21 containers runtime
- Tests performance Gateway vs direct requis