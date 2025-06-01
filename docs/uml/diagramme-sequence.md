# Diagramme de séquence
```` mermaid 
sequenceDiagram
    participant E as Employé
    participant C as Console
    participant V as Vente
    participant P as Produit
    participant DB as Database

    Note over E,DB: Processus d'enregistrement d'une vente

    %% Début de la vente:
    E->>C: Sélectionne "Enregistrer une vente"
    C->>DB: Commence transaction
    
    %% Saisie produit:
    C->>E: Demande ID produit
    E->>C: Saisit ID produit
    C->>P: Vérifie stock disponible
    
    alt Stock disponible
        P->>C: Retourne stock
        C->>E: Demande quantité
        E->>C: Saisit quantité
        
        alt Quantité valide
            C->>V: Crée ligne de vente
            C->>P: Réduit stock
            C->>DB: Sauvegarde transaction
            C->>E: Affiche confirmation
        else Quantité > stock
            C->>E: Erreur: Stock insuffisant
            C->>DB: Annulation transaction
        end
        
    else Stock insuffisant
        C->>E: Annulation - Stock insuffisant
        C->>DB: Rollback automatique
    end
    
    %% Gestion d'erreurs:
    Note over C,DB: Gestion d'Erreurs
    
    alt Produit inexistant
        P-->>C: Produit non trouvé
        C->>E: Message d'erreur
    else Erreur DB
        DB-->>C: Erreur base de données
        C->>DB: Rollback automatique
        C->>E: Message d'erreur système
    end
````
# Séquence d'intéraction pour chaque acteurs et objets en détails:

_Acteurs et Objets:_
Employé: Utilisateur du système
Console: Interface utilisateur
Vente: Objet vente
Produit: Objet produit
Database: Base de données

_Séquence d'Interactions:_
Employé → Console: Sélectionne "Enregistrer une vente"
Console → Database: Commence transaction
Console → Employé: Demande ID produit
Employé → Console: Saisit ID produit
Console → Produit: Vérifie stock disponible
Produit → Console: Retourne stock
Console → Employé: Demande quantité
Employé → Console: Saisit quantité
Console → Vente: Crée ligne de vente
Console → Produit: Réduit stock
Console → Database: Sauvegarde transaction
Console → Employé: Affiche confirmation

_Gestion d'Erreurs:_
Stock insuffisant → Annulation
Erreur DB → Rollback automatique
Produit inexistant → Message d'erreur
