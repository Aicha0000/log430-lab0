## Diagramme de cas d'utilisation
```` mermaid 
graph TB
    Employee[Employé du magasin]
    
    subgraph "Système de caisse POS"
        UC1[Rechercher un produit]
        UC2[Enregistrer une vente]
        UC3[Gérer les retours]
        UC4[Consulter l'état du stock]
        UC5[Ajouter un produit]
    end
    
    Employee --> UC1
    Employee --> UC2
    Employee --> UC3
    Employee --> UC4
    Employee --> UC5
   ```` 
# Cas d'utilisation

Acteurs:
- Employé du magasin: Utilisateur principal du système de caisse

# Cas d'utilisation principaux:

1. Rechercher un produit
- Par ID ou nom de produit
- Consulter stock disponible
2. Enregistrer une vente
- Sélectionner les produit(s)
- Calculer le total
- Mettre à jour le stock
3. Gérer les retours
- Annuler une vente
- Restaurer (mettre a jours) le stock
4. Consulter l'état du stock
- Voir les quantités disponibles
- Notifications par rapport aux stocks
5. Ajouter un produit
- Nouveau produit avec stock initial

# Contraintes

- support de 3 caisses simultanés
- Interface console simple
