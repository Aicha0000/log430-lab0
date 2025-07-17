"""
Modèle Vente pour les rapports consolidés
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Vente:
    """Entité Vente pour UC1 - Rapports consolidés"""
    id: str
    magasin_id: str
    produit_id: str
    quantite: int
    prix_unitaire: float
    total: float
    date_vente: datetime
    
    def __str__(self):
        return f"Vente {self.id}: {self.quantite}x produit {self.produit_id} = ${self.total}"


@dataclass
class RapportVente:
    """Rapport consolidé des ventes pour UC1"""
    periode: str
    ventes_par_magasin: dict
    produits_plus_vendus: list
    stocks_restants: dict
    total_general: float
    
    def __str__(self):
        return f"Rapport {self.periode}: {len(self.ventes_par_magasin)} magasins, Total: ${self.total_general}"
