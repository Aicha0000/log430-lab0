"""
Modèle Produit partagé entre tous les services
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Produit:
    """Entité Produit selon DDD"""
    id: str
    nom: str
    description: str
    prix: float
    stock_central: int = 0
    seuil_critique: int = 10
    updated_at: Optional[datetime] = None
    
    def is_stock_low(self) -> bool:
        """Vérifie si le stock est en dessous du seuil critique"""
        return self.stock_central <= self.seuil_critique
    
    def __str__(self):
        return f"{self.nom} (ID: {self.id}) - Stock: {self.stock_central}"


@dataclass
class DemandeReapprovisionnement:
    """Demande d'approvisionnement d'un magasin - UC2"""
    id: str
    magasin_id: str
    produit_id: str
    quantite_demandee: int
    statut: str = "EN_ATTENTE"  # Options: EN_ATTENTE, APPROUVE, REJETE, TRAITE
    created_at: Optional[datetime] = None
    
    def __str__(self):
        return f"Demande {self.id}: {self.quantite_demandee}x {self.produit_id} pour magasin {self.magasin_id}"
