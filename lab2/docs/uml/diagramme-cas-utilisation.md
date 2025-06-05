## Diagramme de cas d'utilisation
```` mermaid 
graph TB
    Employé Magasin
    Gestionnaire Maison Mère
    Responsable logistique

    subgraph "Système Multi-Magasins"
        UC1[UC1: Générer rapport consolidé]
        UC2[UC2: Consulter stock central]
        UC3[UC3: Tableau de bord]
        UC4[UC4: Mettre à jour produits]
        UC6[UC6: Approvisionner magasin]
        UC7[UC7: Alertes automatiques]
        UC8[UC8: Interface web]
    end

    Gestionnaire Maison Mère --> UC1
    Employé Magasin --> UC2
    Gestionnaire Maison Mère --> UC3
    Gestionnaire Maison Mère --> UC4
    Responsable logistique --> UC6
    UC7 -.-> Gestionnaire Maison Mère
    Gestionnaire Maison Mère --> UC8
   ```` 
# Cas d'utilisation
Acteurs:
Employé Magasin : Consulte les stocks, faire les demandes de réapprovisionnement
Gestionnaire Maison Mère : Génère des rapports, supervise les performances, gère les produits
Responsable Logistique : Valide et traite les approvisionnements entre entrepôt et magasins

# Cas d'utilisation principaux:
Must Have:
UC1 : Générer un rapport consolidé des ventes par magasin
UC2 : Consulter le stock central et déclencher un réapprovisionnement
UC3 : Visualiser les performances dans un tableau de bord
Should Have:
UC4 : Mettre à jour les produits depuis la maison mère
UC6 : Approvisionner un magasin depuis le centre logistique
Could Have:
UC7 : Alerter automatiquement en cas de rupture critique
UC8 : Interface web minimale pour les gestionnaires

# Contraintes
Cohérence des données : Synchronisation entre magasins et maison mère
Temps réel : Les alertes doivent être transmises rapidement
Autonomie locale : Les magasins doivent fonctionner même en cas de panne réseau