# ADR-002: Stratégie de communication inter-services: REST + Event (Webhooks HTTP)

## Status
Acceptée par Aicha Aanounou

## Date 
30 Mai 2025

## Context
Le système distribué (5 magasins + entrepôt + maison mère) nécessite une stratégie de communication pour synchroniser les stocks, déclencher les réapprovisionnements, générer les rapports consolidés et assurer les alertes automatiques (UC7). La communication doit supporter à la fois les requêtes synchrones directes et les notifications asynchrones.

## Décision
API REST pour les communications synchrones + HTTP Webhooks pour les événements asynchrones. Utilisation de FastAPI pour les endpoints REST et système de webhooks pour les notifications temps réel (UC7).

## Alternatives considérées
- Seulement API REST: Simple mais pas de notifications push, problèmes de cascade de pannes

## Justification
- Webhooks HTTP offrent le meilleur équilibre simplicité/efficacité pour ce laboratoire. Il permet les notifications temps réel (UC7) sans infrastructure additionnelle. Communication REST naturelle pour UC1, UC2, UC3, UC4, UC6 qui requiert une requête directe.

## Conséquences positives ou négatives acceptées
- Notifications temps réel pour les alertes automatiques, aucune infrastructure additionnelle est requise
- Pas de garantie de livraison

