## Diagramme de deploiement
```` mermaid 
graph TB
    subgraph "Infrastructure de Déploiement"
        subgraph "Maison Mère"
            postgres[(PostgreSQL Central)]
            administration[administration]
            web[web-minimal]
        end
        
        subgraph "Les magasins"
            subgraph "Magasin Type"
                sqlite[(SQLite Local)]
                magasin[magasin]
                magasin --> sqlite
        end

        subgraph "Centre Logistique"
            logistique[logistique]
        end
    end
 
    %% Communication réseau
    magasin -.-> administration : "REST + Webhooks"
    magasin -.-> logistique : "REST"
    logistique -.-> administration : "REST + Webhooks"
    administration --> postgres
     ```` 