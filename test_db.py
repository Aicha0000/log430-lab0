"""
Ce fichier est un test temporaire pour la creation & conneion de la base de donnees
"""

from app.models import Produit
from app.persistance.bd import session

#Creation d'un produit test
p = Produit(nom="Ice Tea", prix=7.50, description="Boisson rafraichissante")

#Ajout du produit a la session
session.add(p)

#Commit de la session pour enregistrer le produit dans la base de donnees
session.commit()

#Lire tous les produits et les afficher
produit = session.query(Produit).all()
for produit in produit:
    print(produit)
