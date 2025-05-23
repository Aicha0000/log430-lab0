"""
Fichier console qui est l'interface console du système de caisse.
"""

from app.models import Produit
from app.persistance.db import session

def afficher_console_menu():
    """Affiche le menu principal de l'application."""
    print("Bienvenue dans le Menu Caisse")
    print("1. Ajouter un produit")
    print("2. Afficher les produits")
    print("3. Supprimer un produit")
    print("4. Quitter")

def ajouter_produit():
    """Demande les infos d’un produit et l’ajoute à la base."""
    nom = input("Entrez le nom du produit : ")
    prix = float(input("Prix: "))
    description = input("Description: ") 
    produit = Produit(nom=nom, prix=prix, description=description)
    session.add(produit)
    session.commit()
    print(f"Produit '{nom}' ajouté.")

def afficher_produits():
    """Affiche tous les produits en base de données."""
    produits = session.query(Produit).all()
    for produit in produits:
        print(f"ID: {produit.id}, Nom: {produit.nom}, "
              f"Prix: {produit.prix}, Description: {produit.description}")

def main():
    """Point d'entrée principal de l’application console."""
    while True:
        afficher_console_menu()
        choix = input("Choisissez une option : ")

        if choix == '1':
            ajouter_produit()
        elif choix == '2':
            afficher_produits()
        elif choix == '3':
            break
        else:
            print("Choix invalide, essayez à nouveau.")

if __name__ == "__main__":
    main()
