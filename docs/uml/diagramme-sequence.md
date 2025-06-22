# Diagramme de Sequence - pour UC1 a UC6

## UC1: Generation Rapport

```mermaid
sequenceDiagram
    participant G as Gestionnaire
    participant IG as ConsoleGestionnaire
    participant RC as RapportsConsolides
    participant VR as VenteRepository

    G->>IG: generer_rapport_consolide()
    IG->>RC: generer_rapport_consolide(30)
    RC->>VR: get_total_ventes_par_magasin()
    RC->>VR: get_produits_plus_vendus(5)
    VR-->>RC: donnees_ventes
    RC-->>IG: RapportVente
    IG->>RC: afficher_rapport_detaille()
    IG-->>G: Rapport affiche
```

## UC2: Consultation Stock et Demande Reapprovisionnement

```mermaid
sequenceDiagram
    participant E as Employe
    participant IC as ConsoleEmployeMagasin
    participant GS as GestionStocks
    participant SR as StockRepository

    E->>IC: consulter_stock_produit()
    IC->>E: Demander ID produit
    E->>IC: "1"
    
    IC->>GS: get_stock("1")
    GS->>SR: get_produit_by_id("1")
    SR-->>GS: Produit
    GS-->>IC: Produit
    
    IC->>E: Afficher stock
    E->>IC: Demander reappro
    
    IC->>SR: create_demande_reapprovisionnement()
    SR-->>IC: success
    IC-->>E: "Demande envoyee"
```

## UC3: Tableau de Bord

```mermaid
sequenceDiagram
    participant G as Gestionnaire
    participant IG as ConsoleGestionnaire
    participant TB as TableauBordService
    participant RC as RapportsConsolides
    participant GS as GestionStocks

    G->>IG: afficher_tableau_bord()
    IG->>TB: generer_tableau_bord()
    
    TB->>RC: generer_rapport_consolide(30)
    RC-->>TB: rapport_base
    
    TB->>GS: lister_tous_produits()
    GS-->>TB: liste_produits
    
    TB->>TB: _detecter_alertes_stock()
    TB->>TB: _calculer_performances_magasins()
    
    TB-->>IG: tableau_bord
    IG->>TB: afficher_tableau_bord(dashboard)
    IG-->>G: Dashboard affiche
```

## UC4: Modification Produit

```mermaid
sequenceDiagram
    participant G as Gestionnaire
    participant IG as ConsoleGestionnaire
    participant GP as GestionProduitsService
    participant SR as StockRepository

    G->>IG: gerer_produits()
    IG->>IG: afficher_menu_produits()
    G->>IG: "2" (modifier produit)
    
    IG->>GP: lister_produits()
    GP->>SR: get_all_produits()
    SR-->>GP: liste_produits
    GP-->>IG: produits
    
    IG->>G: Afficher produits
    G->>IG: ID + nouvelles_donnees
    
    IG->>GP: modifier_produit(id, nom, prix)
    GP->>SR: update_product(id, donnees)
    SR-->>GP: success
    GP->>GP: _synchroniser_vers_magasins()
    GP-->>IG: success
    IG-->>G: "Produit modifie"
```

## UC6: Traitement Reapprovisionnement

```mermaid
sequenceDiagram
    participant RL as ResponsableLogistique
    participant IL as InterfaceLogistique
    participant RS as ReapprovisionnementService
    participant SR as StockRepository

    RL->>IL: gerer_reapprovisionnement()
    IL->>IL: afficher_menu()
    RL->>IL: "2" (traiter demande)
    
    IL->>RS: lister_demandes_en_attente()
    RS->>SR: get_demandes_reapprovisionnement()
    SR-->>RS: demandes
    RS-->>IL: demandes_en_attente
    
    IL->>RL: Afficher demandes
    RL->>IL: Selectionner demande
    
    IL->>RS: approuver_et_traiter(demande_id)
    RS->>SR: get_produit_by_id()
    SR-->>RS: produit
    RS->>RS: valider_stock_suffisant()
    RS->>SR: update_stock()
    RS->>SR: update_demande_statut("TRAITE")
    SR-->>RS: success
    RS-->>IL: true
    IL-->>RL: "Demande traitee"
```
