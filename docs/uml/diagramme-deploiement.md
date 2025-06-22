## Diagramme de deploiement

```mermaid
graph TB
    subgraph "Infrastructure de Deploiement"
        subgraph "Maison Mere"
            postgres[(PostgreSQL Central)]
            administration[Administration]
            web[Web Minimal]
        end
        
        subgraph "Les Magasins"
            subgraph "Magasin Type"
                sqlite[(SQLite Local)]
                magasin[Magasin]
                magasin --> sqlite
            end
        end

        subgraph "Centre Logistique"
            logistique[Logistique]
        end
    end
 
    %% Communication reseau
    magasin -.-> administration : "REST + Webhooks"
    magasin -.-> logistique : "REST"
    logistique -.-> administration : "REST + Webhooks"
    administration --> postgres
``` 