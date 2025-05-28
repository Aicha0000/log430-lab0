# Diagramme de déploiement: Architecture 2-Tiers
```` mermaid 
graph TB
    subgraph "Machine Locale/VM"
        subgraph "Conteneur Docker - Application"
            App[Application Console Python]
            Menu[Interface utilisateur<br/>menu console]
            App --> Menu
        end
        
        subgraph "Conteneur Docker - Base de données"
            DB[(Base de données SQLite<br/>bd.sqlite)]
        end
        
        subgraph "3 Caisses Simultanées"
            Caisse1[Caisse 1]
            Caisse2[Caisse 2] 
            Caisse3[Caisse 3]
        end
    end
    
    App --> DB
    Caisse1 --> App
    Caisse2 --> App
    Caisse3 --> App
    
    %% Annotations:
    App -.->|"Accès direct<br/>au fichier SQLite"| DB
    DB -.->|"Stockage des données<br/>persistantes"| DB
 ```` 
    
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
