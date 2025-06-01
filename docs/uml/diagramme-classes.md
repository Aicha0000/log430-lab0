# Class Diagram

```` mermaid 

class Produit {
    +id: Integer
    +nom: String(50)
    +prix: Float
    +description: String(100)
    +stock: Integer
}

class Vente {
    +id: Integer
    +date_vente: DateTime
    +total: Float
    +statut: String(20)
}

class LigneVente {
    +id: Integer
    +vente_id: Integer
    +produit_id: Integer
    +quantite: Integer
    +prix_unitaire: Float
}

    Vente "1" --> "*" LigneVente : contient
    LigneVente "*" --> "1" Produit : référence
```` 