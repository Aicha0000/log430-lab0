# Diagramme d'implementation

```mermaid
graph TB
    subgraph "Structure du Laboratoire 2"
        subgraph "Couche Commun"
          repositories[repositories/]
          modeles[modeles/]
          repositories --> modeles
        end
    
        subgraph "Couches Services"
            subgraph "Magasin"
                magasin_repositories[repositories/]
                magasin_logique[gestion_ventes.py]
                magasin_console[interface_console.py]
            end
            
            subgraph "Logistique" 
                logistique_repositories[repositories/]
                logistique_logique[gestion_stocks.py]
                logistique_reapprovisionnement[reapprovisionnement.py]
                logistique_alerts[alertes_automatiques.py]
            end
            
            subgraph "Administration"
                administration_repositories[repositories/]
                administration_rapports[rapports_consolides.py]
                administration_tableau_bord[tableau_bord.py]
                administration_produits[gestion_produits.py]
            end

            subgraph "Web Minimal"
                web_routes[routes_gestionnaires.py]
                web_static[static/]
                web_templates[templates/]
            end
        end
    end
    
    %% Dependances
    magasin_repositories -.-> repositories
    logistique_repositories -.-> repositories
    administration_repositories -.-> repositories

    magasin_logique --> magasin_repositories
    logistique_logique --> logistique_repositories
    administration_rapports --> administration_repositories
``` 
## Structure du Laboratoire 2

### Couches Logiciels

**1. Couche Presentation:**
- Interface Console : Interaction employes magasin (Python CLI)
- Interface Web : Dashboard gestionnaires (HTML/CSS/JS templates)
- API REST : Endpoints services pour communication inter-services

**2. Couche Application (Services):**
- magasin-service : Logique ventes locales, gestion caisses
- logistique-service : Logique stocks, reapprovisionnement, alertes
- administration-service : Logique rapports, consolidation, gestion produits

**3. Couche Repository (Patron):**
- Interfaces Repository : Abstraction acces donnees (ProductRepository, VenteRepository)
- Implementations : Repository concrets pour local (SQLite) et central (PostgreSQL)

**4. Couche Persistance:**
- PostgreSQL Central : Catalogue produits, rapports consolides, configuration
- SQLite Local : Ventes quotidiennes, stocks magasin

### Dependances
- Synchrone : API REST pour requetes directes (UC1, UC2, UC3)
- Asynchrone : HTTP Webhooks pour evenements (UC7 alertes)

### Technologies d'Implementation
- Docker : Conteneurisation services
- PostgreSQL 15 : Base centrale (catalogue, rapports)
- SQLite 3 : Bases locales par magasin (autonomie)
- SQLAlchemy : ORM pour abstraction base de donnees
- pytest : Tests unitaires et integration
- GitHub Actions : Pipeline CI/CD automatisee
