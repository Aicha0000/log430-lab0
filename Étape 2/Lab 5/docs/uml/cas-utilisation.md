# Diagramme de Cas d'Utilisation

```mermaid
graph TD
    Client((Client))
    Admin((Administrateur))
    
    GererCompte[Gerer Compte]
    ConsulterBoissons[Consulter Boissons]
    GererPanier[Gerer Panier]
    PasserCommande[Passer Commande]
    ValiderCheckout[Valider Checkout]
    
    ConfigurerServices[Configurer Services]
    MonitorerSysteme[Monitorer Systeme]
    GererInventory[Gerer Inventory]
    VoirReports[Voir Reports]
    AnalyserVentes[Analyser Ventes]
    
    Client --> GererCompte
    Client --> ConsulterBoissons
    Client --> GererPanier
    Client --> PasserCommande
    Client --> ValiderCheckout
    
    Admin --> ConfigurerServices
    Admin --> MonitorerSysteme
    Admin --> GererInventory
    Admin --> VoirReports
    Admin --> AnalyserVentes
    
    classDef actor fill:#e1f5fe,stroke:#01579b,stroke-width:3px,color:#000000,font-size:14px,font-weight:bold
    classDef usecase fill:#f3e5f5,stroke:#4a148c,stroke-width:2px,color:#000000,font-size:12px,font-weight:bold
    
    class Client,Admin actor
    class GererCompte,ConsulterBoissons,GererPanier,PasserCommande,ValiderCheckout,ConfigurerServices,MonitorerSysteme,GererInventory,VoirReports,AnalyserVentes usecase
```