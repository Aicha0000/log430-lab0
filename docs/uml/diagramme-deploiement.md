# Diagramme de déploiement: Architecture 2-Tiers

# Tier 1 - Client:
- Application Console Python
- Interface utilisateur (menu console)

# Tier 2 - Serveur:
- Base de données SQLite
- Stockage des données persistantes

# Architecture 
Client (Python App) ←→ Serveur (SQLite Database)

# Déploiement
- Environnement: Container Docker
- Communication: Accès direct au fichier SQLite
- Concurrence: Support de 3 caisses simultanées
- Persistance: Fichier bd.sqlite