"""
Repository Pattern - Interface pour la gestion des stocks
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from ..modeles.produit import Produit, DemandeReapprovisionnement


class StockRepository(ABC):
    """Interface pour accès aux données stock - Repository Pattern"""
    
    @abstractmethod
    def get_produit_by_id(self, produit_id: str) -> Optional[Produit]:
        """UC2: Consulter un produit spécifique par son ID"""
        pass
    
    @abstractmethod
    def get_all_produits(self) -> List[Produit]:
        """UC2: Consulter tous les produits disponibles"""
        pass
    
    @abstractmethod
    def search_produits(self, terme_recherche: str) -> List[Produit]:
        """UC2: Rechercher des produits par nom"""
        pass
    
    @abstractmethod
    def get_stock_disponible(self, produit_id: str) -> int:
        """UC2: Obtenir le stock disponible pour un produit"""
        pass
    
    @abstractmethod
    def create_demande_reapprovisionnement(self, demande: DemandeReapprovisionnement) -> bool:
        """UC2: Créer une demande de réapprovisionnement"""
        pass
    
    @abstractmethod
    def get_produits_low_stock(self, seuil: int = 10) -> List[Produit]:
        """UC7: Produits avec stock faible pour alertes automatiques"""
        pass
