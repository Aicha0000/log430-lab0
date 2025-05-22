"""Ce module définit les entités du système de caisse."""

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Produit(Base):  # pylint: disable=too-few-public-methods
    """Classe qui représente un produit.
    
    Attributs:
        id: Identifiant unique du produit
        nom: Nom du produit
        prix: Prix unitaire du produit
        description: Catégorie du produit
    """

    __tablename__ = 'produits'

    id = Column(Integer, primary_key=True)
    nom = Column(String(50), nullable=False)
    prix = Column(Float, nullable=False)
    description = Column(String(100), nullable=True)

    def __repr__(self):
        """Représentation string du produit pour le débogage."""
        return (f"<Produit(id={self.id}, nom='{self.nom}', "
                f"prix={self.prix}, description='{self.description}')>")
    