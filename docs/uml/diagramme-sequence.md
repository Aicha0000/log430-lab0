# Diagramme de séquence

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
