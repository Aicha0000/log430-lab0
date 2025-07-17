# ADR-001: Choix du Load Balancer

## Status
Accepted

## Context
Le systeme multi-magasins a besoin d'un load balancer pour distribuer le trafic entre plusieurs instances API. On doit choisir entre NGINX, HAProxy, ou Traefik.

## Decision
On utilise NGINX comme load balancer.

## Rationale
- NGINX est simple a configurer avec Docker
- Round-robin par defaut marche bien pour notre cas
- Leger en ressources
- Bon pour servir du contenu statique aussi
- Documentation complete

## Consequences
- Configuration basique avec upstream
- Facile a troubleshoot
- Pas de features avancees mais suffisant pour le lab
- Monitoring avec nginx_status endpoint