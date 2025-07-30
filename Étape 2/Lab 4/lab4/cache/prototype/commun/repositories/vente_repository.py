"""
Patron Repository - Interface pour la gestion des ventes
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from datetime import datetime
from ..modeles.vente import Vente, RapportVente


class VenteRepository(ABC):
    """Interface pour accès aux données ventes"""
    
    @abstractmethod
    def get_ventes_by_magasin(self, magasin_id: str) -> List[Vente]:
        """UC1: Récupérer toutes les ventes d'un magasin"""
        pass
    
    @abstractmethod
    def get_ventes_by_periode(self, date_debut: datetime, date_fin: datetime) -> List[Vente]:
        """UC1: Récupérer les ventes sur une période"""
        pass
    
    @abstractmethod
    def get_total_ventes_par_magasin(self) -> Dict[str, float]:
        """UC1: Total des ventes par magasin"""
        pass
    
    @abstractmethod
    def get_produits_plus_vendus(self, limite: int = 10) -> List[tuple]:
        """UC1: Produits les plus vendus (produit_id, quantité_totale)"""
        pass
