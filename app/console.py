"""
Fichier console qui est l'interface console du système de caisse
"""

from app.models import Produit
from app.persistance.db import session

def afficherConsoleMenu():
    print("Bienvenue dans le Menu Caisse")
    print("1. Ajouter un produit")
    print("2. Afficher les produits")
    print("3. Supprimer un produit")
    print("4. Quitter")

def ajouterProduit():
    nom = input("Entrez le nom du produit : ")
    prix = float(input("Prix: "))
    description = int(input("Description: "))
    
    produit = Produit(nom=nom, prix=prix, description=description)
    session.add(produit)
    session.commit()
    print(f"Produit {nom} ajouté.")

def afficherProduits():
    produits = session.query(Produit).all()
    for produit in produits:
        print(f"ID: {produit.id}, Nom: {produit.nom}, "
              f"Prix: {produit.prix}, Description: {produit.description}")
              
def main():
    while True:
        afficherConsoleMenu()
        choix = input("Choisissez une option : ")
        
        if choix == '1':
            ajouterProduit()
        elif choix == '2':
            afficherProduits()
        elif choix == '3':
            break
        else:
            print("Choix invalide, essayez à nouveau.")

if __name__ == "__main__":
    main()
    