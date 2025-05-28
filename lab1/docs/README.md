# Document Technique du Laboratoire 1
Ce dossier contient la documentation d'architecture et de conception du système de caisse selon le modèle 4+1.

## Architecture Decision Records (ADRs)

adr/plateforme.md - Choix de la plateforme de développement
adr/strategie-persistance.md - Stratégie de persistance et ORM

## Diagrammes UML (Modèle 4+1)

uml/diagramme-cas-utilisation.md - Vue des cas d'utilisation
uml/diagramme-classes.md - Vue logique (modèle de données)
uml/diagramme-deploiement.md - Vue de déploiement (architecture 2-tiers)
uml/diagramme-implementation.md - Vue d'implémentation (organisation des modules)
uml/diagramme-sequence.md - Vue des processus (interactions)

## Architecture du Système
Architecture 2-tiers : Application console Python + Base de données SQLite
Technologies : Python 3.11, SQLAlchemy, Docker, GitHub Actions
Fonctionnalités : Gestion produits, ventes, retours, stocks avec support de 3 caisses simultanées
## Étapes à suivre pour la compréhension du laboratoire 1

1. Commencez par les ADRs pour comprendre les décisions d'architecture
2. Consultez les diagrammes UML pour voir la conception détaillée
3. Référez-vous au README principal pour l'installation et l'utilisation
