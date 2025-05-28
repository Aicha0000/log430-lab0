# ADR-005: Choix du patron de Repository

## Status
Acceptée par Aicha Aanounou

## Date 
30 Mai 2025

## Contexte
L'architecture de la persistance (ADR-003) utilise PostgreSQL central et SQLite local. Les services métier doivent accéder aux données sans connaître leur localisation (locale vs centrale). Besoin d'une abstraction claire pour faciliter les tests et l'évolutivité.

## Décision
Application du Patron Repository uniquement pour abstraire l'accès aux données. Chaque type de donnée aura une interface Repository avec des implémentations pour sources locales et centrales.

## Alternatives considérées
Plusieurs autres patrons peuvent être utilisés soit en collaboration ou de façon unique pour ce laboratoire. L'option d'opter pour le patron Repository est un choix personnel basé sur la matière vu en cours et mes préférences d'implémentation. 

## Justification
Le Repository Pattern résout directement les défis de l'architecture stratifiée (plusieurs couches) :
- Abstrait la complexité central/local (ADR-003)
- Facilite les tests (mock des repositories)

## Conséquences positives ou négatives acceptées
- Tests simplifiés, la logique métier est découplée de la persistance
- Plus de fichiers à maintenier
