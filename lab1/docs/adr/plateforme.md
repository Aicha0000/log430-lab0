## Status
Accepté par Aicha Aanounou
## Date 
24 Mai 2025
## Contexte
Pour le développement du système de caisse en architecture 2-tiers, nous devons choisir une plateforme de développement rapide avec couche de persistance abstraite.
# Décision 
Python 3.11 + SQLAlchemy
## Alternatives considérées
Java + Hibernate (trop complexe pour ce lab)
## Justification
- Développement rapide et simple
- SQLAlchemy: ORM mature pour abstraction persistance
- Facile à conteneuriser avec Docker
- Simple pour mon prototypage
## Conséquences positives ou négatives acceptées
- Code simple, développement accéléré, déploiement facile
- Performance moindre mais acceptable
