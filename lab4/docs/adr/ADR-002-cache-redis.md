# ADR-002: Cache Redis Distribue

## Status
Accepted

## Context
Les endpoints /api/central et /api/consolide sont lents et sollicites. Il faut un cache pour ameliorer les performances.

## Decision
On utilise Redis comme cache distribue.

## Rationale
- Redis est rapide et fiable
- Cache distribue = partage entre instances API
- TTL automatique pour expiration
- Facile a deployer avec Docker
- Patterns d'invalidation simples

## Consequences
- Cache hit = reponse immediate
- Cache miss = query DB + set cache
- Invalidation sur PUT /api/produits
- Single point of failure (pas de cluster)
- Amelioration significative des performances