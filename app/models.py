""" 
Ce Modules definit les entites du systeme de caisse
"""

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()
# pylint: disable=too-few-public-methods
class Produit(Base):
    """ 
    Classe qui represente un produit 
    Mes attributs sont:
    id = Identifiant unique du produit
    nom = nom du produit
    prix = Prix unitaire du produit
    description = Categorie du produit
      """

    __tablename__ = 'produits'

    id = Column(Integer, primary_key=True)
    nom = Column(String(50), nullable=False)
    prix = Column(Float, nullable=False)
    description = Column(String(100), nullable=True)

    def __repr__(self):
        return (f"<Produit(id={self.id}, nom='{self.nom}', prix={self.prix}, "
                f"description='{self.description}')>")
