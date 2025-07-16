# ADR-002: Load Balancing Strategy

## Status
Accepted

## Context
Lab 5 demande mise en place load balancing pour au moins un microservice. Cart-service est bon candidat car:
- Service e-commerce avec potentiel trafic elevé
- Operations lecture/ecriture simples
- Peu de state partagé

## Decision
Implémenter load balancing round-robin pour cart-service avec 3 instances via Kong Gateway.

## Rationale
- **Round-robin**: simple et efficace pour charge uniforme
- **3 instances**: équilibre entre redondance et ressources
- **Cart-service choisi**: operations stateless, shared database
- **Kong upstream**: gestion automatique failover
- **Database partagée**: toutes instances accèdent même cart-db

## Implementation
- 3 containers cart-service dans docker-compose
- Kong upstream avec targets vers chaque instance  
- Health checks automatiques
- Metrics Prometheus pour monitoring distribution

## Consequences
**Positif:**
- Meilleure resilience si une instance fail
- Distribution charge automatique
- Monitoring trafic par instance possible

**Negatif:**
- Plus de ressources consommées  
- Complexite setup Kong upstream
- Database devient bottleneck potentiel

## Tests
- K6/JMeter pour verifier distribution requests
- Grafana dashboard pour visualiser metrics par instance
- Tests failover: kill une instance, verifier routing