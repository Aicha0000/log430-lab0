## Status
Accepté par Aicha Aanounou
## Date
24 Mai 2025
## Contexte
Le système de caisse doit persister les données (produits, ventes, stocks) de manière fiable avec support des transactions pour 3 caisses simultanées.
## Décision
ORM avec SQLAlchemy
## Alternative considérées
- SQL pour augmenter la performance mais le code deviendrait
trop complexe
## Justification
- Gestion native des transactions ACID
- Code plus maintenable et lisible avec ORM et SQLALchemy
## Conséquences positives ou négatives acceptées
- gestion automatique des relations, transactions faciles
- Légère perte de performance
