"""
Ce module définit les entités du système de caisse.
"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class Produit(Base):  # pylint: disable=too-few-public-methods
    """
    Classe représentant un produit.
    """
    __tablename__ = 'produits'
    
    id = Column(Integer, primary_key=True)
    nom = Column(String(50), nullable=False)
    prix = Column(Float, nullable=False)
    description = Column(String(100), nullable=True)
    stock = Column(Integer, default=0, nullable=False)
    
    def __repr__(self):
        return f"<Produit(id={self.id}, nom='{self.nom}', prix={self.prix}, stock={self.stock})>"


class Vente(Base):  # pylint: disable=too-few-public-methods
    """
    Classe représentant une vente.
    """
    __tablename__ = 'ventes'
    
    id = Column(Integer, primary_key=True)
    date_vente = Column(DateTime, default=datetime.now, nullable=False)
    total = Column(Float, nullable=False)
    statut = Column(String(20), default='active', nullable=False)  # active ou annulee
    
    lignes = relationship("LigneVente", back_populates="vente")


class LigneVente(Base):  # pylint: disable=too-few-public-methods
    """
    Classe représentant une ligne de vente.
    """
    __tablename__ = 'lignes_vente'
    
    id = Column(Integer, primary_key=True)
    vente_id = Column(Integer, ForeignKey('ventes.id'), nullable=False)
    produit_id = Column(Integer, ForeignKey('produits.id'), nullable=False)
    quantite = Column(Integer, nullable=False)
    prix_unitaire = Column(Float, nullable=False)
    
    vente = relationship("Vente", back_populates="lignes")
    produit = relationship("Produit")
    