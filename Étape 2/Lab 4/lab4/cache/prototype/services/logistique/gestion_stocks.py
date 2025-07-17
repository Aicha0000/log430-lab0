
from typing import List, Optional

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from commun.modeles.produit import Produit
from commun.repositories.stock_repository import StockRepository


class GestionStocks:
    
    def __init__(self, stock_repository: StockRepository):
        self.stock_repo = stock_repository
    
    def get_stock(self, produit_id: str) -> Optional[Produit]:
        produit = self.stock_repo.get_produit_by_id(produit_id)
        if produit:
            print(f"Stock central - {produit}")
            return produit
        else:
            print(f"Produit {produit_id} non trouvé")
            return None
    
    def search(self, terme: str) -> List[Produit]:
        produits = self.stock_repo.search_produits(terme)
        print(f"{len(produits)} produits pour '{terme}'")
        for p in produits:
            status = "FAIBLE" if p.is_stock_low() else "OK"
            print(f"- {p} ({status})")
        return produits
    
    def list_all(self) -> List[Produit]:
        produits = self.stock_repo.get_all_produits()
        print(f"{len(produits)} produits:")
        for p in produits:
            status = "FAIBLE" if p.is_stock_low() else "OK"
            print(f"- {p} ({status})")
        return produits
    
    def consulter_stock_central(self, produit_id: str) -> Optional[Produit]:
        return self.get_stock(produit_id)
    
    def rechercher_produits(self, terme: str) -> List[Produit]:
        return self.search(terme)
    
    def lister_tous_produits(self) -> List[Produit]:
        return self.list_all()

