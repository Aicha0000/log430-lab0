# ADR-001: choix d'architecture: Domain-Driven Design

## Status
Acceptée par Aicha Aanounou

## Date 
30 Mai 2025

## Context
Le système doit gérer plusieurs concepts métier distincts avec des règles d'affaires et des cycles de vie différents :
- Ventes locales par magasin (transactions quotidiennes)
- Gestion des stocks (magasins + entrepôt, réapprovisionnement)
- Rapports consolidés (supervision maison mère)
- Catalogue produits centralisé (gestion centralisée)

## Décisions
L'identification des 4 bounded contexts:
- **Context Magasin** : Ventes locales, stock local, employés
- **Context Logistique** : Entrepôt, réapprovisionnement, transferts
- **Context Administration** : Rapports, configuration, supervision

## Alternatives considérées
1) L'option de l'architecture en microservice mais ce n'est pas optimal puisque c'est trop complex, voir un overkill pour ce laboratoire qui ne requiert que 7 sites (5 magasins + 1 entrepôt et une maison mère)
2) L'option de monolithe modulaire n'est pas optimal dans ce cas-ci puisqu'elle ne permet pas de consulter le stock central via un magasin. De plus, une simple panne causera l'arrêt de l'ensemble des magasins de ventes.

## Justification
Domain-Driven Design (DDD)
Chaque cas d'usage (UC1-UC8) s'aligne naturellement avec un contexte métier spécifique. Les règles d'affaires diffèrent entre ventes, gestion des stocks, et supervision centralisée permet de répondre à l'ensemble des besoins du laboratoire. De plus, la facilité d'ajout futur de magasins avec cette approche assure une implémentation sans trop de complexité.

## Conséquences positives ou négatives acceptées
- Facilité à faire l'ajout de plus de magasins plustard, séparation claire des métiers, indépendance de chaque système, plus facile à maintenir dans le cas d'une panne
- Duplication potentielle de certaines entités, requiert une très bonne connaissance de chaque domaine

