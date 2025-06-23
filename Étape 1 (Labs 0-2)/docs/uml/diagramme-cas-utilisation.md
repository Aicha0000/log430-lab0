## Diagramme de cas d'utilisation

```mermaid
graph TB
    EM["Employe Magasin"]
    GMM["Gestionnaire Maison Mere"]
    RL["Responsable Logistique"]

    subgraph "Systeme Multi-Magasins"
        UC1["UC1: Generer rapport consolide"]
        UC2["UC2: Consulter stock central"]
        UC3["UC3: Tableau de bord"]
        UC4["UC4: Mettre a jour produits"]
        UC6["UC6: Approvisionner magasin"]
        UC7["UC7: Alertes automatiques"]
        UC8["UC8: Interface web"]
    end

    GMM --> UC1
    EM --> UC2
    GMM --> UC3
    GMM --> UC4
    RL --> UC6
    UC7 -.-> GMM
    GMM --> UC8
``` 
## Cas d'utilisation

**Acteurs:**
- Employe Magasin : Consulte les stocks, fait les demandes de reapprovisionnement
- Gestionnaire Maison Mere : Genere des rapports, supervise les performances, gere les produits
- Responsable Logistique : Valide et traite les approvisionnements entre entrepot et magasins

**Cas d'utilisation principaux:**

*Must Have:*
- UC1 : Generer un rapport consolide des ventes par magasin
- UC2 : Consulter le stock central et declencher un reapprovisionnement
- UC3 : Visualiser les performances dans un tableau de bord

*Should Have:*
- UC4 : Mettre a jour les produits depuis la maison mere
- UC6 : Approvisionner un magasin depuis le centre logistique

*Could Have:*
- UC7 : Alerter automatiquement en cas de rupture critique
- UC8 : Interface web minimale pour les gestionnaires

**Contraintes**
- Coherence des donnees : Synchronisation entre magasins et maison mere
- Temps reel : Les alertes doivent etre transmises rapidement
- Autonomie locale : Les magasins doivent fonctionner meme en cas de panne reseau