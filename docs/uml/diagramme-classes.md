# Class Diagram

```` mermaid 
classDiagram
    class Produit {
        +int id
        +string nom
        +float prix
        +string description
        +int stock
    }
    
    class Vente {
        +int id
        +datetime date_vente
        +float total
        +string statut
    }
    
    class LigneVente {
        +int id
        +int vente_id
        +int produit_id
        +int quantite
        +float prix_unitaire
    }
    
    %% Relations:
    Vente "1" --> "*" LigneVente : contient
    LigneVente "*" --> "1" Produit : référence
```` 
