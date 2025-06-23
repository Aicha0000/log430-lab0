# ADR-003: Stratégie de persistance des données: PostgreSQL

## Status
Acceptée par Aicha Aanounou

## Date 
30 Mai 2025

## Context
Le système doit gérer les données de 5 magasins + entrepôt + maison mère. 
- Nécessité de maintenir la cohérence pour les rapports consolidés (UC1, UC3)
- Assurer l'autonomie des magasins lors de pannes réseau
-  Les données ont des cycles de vie et des besoins de cohérence différents

## Décision
PostgreSQL pour la maison mère et pour les magasins avec l'application du Repository Pattern uniquement pour abstraire l'accès aux données (voir ADR 005-patron.md)

## Alternatives considérées
PostgreSQL central pour données de référence et rapports ainsi que pour l'autonomie opérationnelle des magasins. La synchronisatioin se fait via APIs et webhooks.

## Justification
Cette stratégie de persistance permet l'autonomie locale (ventes continuent si réseau coupé) tout en conservant la capacité de génération de rapports consolidés (UC1, UC3). Les données des magasins sont centralisées (UC4) avec la possibilité d'une cache local pour la performance. 

## Conséquences positives ou négatives acceptées
- Rapport consolidés simple avec la centralisation des données
- Complexité de synchronisation à gérer, Monitoring de la cohérence nécessaire

