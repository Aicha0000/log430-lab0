"""
Patron Repository - Interface pour la gestion des stocks
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from ..modeles.produit import Produit, DemandeReapprovisionnement


class StockRepository(ABC):
    
    @abstractmethod
    def get_produit_by_id(self, produit_id: str) -> Optional[Produit]:
        pass
    
    @abstractmethod
    def get_all_produits(self) -> List[Produit]:
        pass
    
    @abstractmethod
    def search_produits(self, terme_recherche: str) -> List[Produit]:
        pass
    
    @abstractmethod
    def create_demande_reapprovisionnement(self, demande: DemandeReapprovisionnement) -> bool:
        pass