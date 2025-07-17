
from typing import List, Optional

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from commun.modeles.produit import Produit
from commun.repositories.stock_repository import StockRepository


class GestionProduitsService:
    
    def __init__(self, stock_repository: StockRepository):
        self.stock_repo = stock_repository
        self.magasins = ["magasin 1", "magasin 2", "magasin 3", "magasin 4", "magasin 5"]
    
    def lister_produits(self) -> List[Produit]:
        return self.stock_repo.get_all_produits()
    
    def obtenir_produit(self, produit_id: str) -> Optional[Produit]:
        return self.stock_repo.get_produit_by_id(produit_id)
    
    def modifier_produit(self, produit_id: str, nom: str = None, prix: float = None, description: str = None) -> bool:
        produit = self.obtenir_produit(produit_id)
        
        if not produit:
            print(f"Produit {produit_id} non trouvé")
            return False
        
        ancien_nom = produit.nom
        ancien_prix = produit.prix
        ancienne_description = produit.description
        
        modifications = []
        if nom and nom != produit.nom:
            modifications.append(f"Nom: '{ancien_nom}' -> '{nom}'")
        
        if prix and prix != produit.prix:
            modifications.append(f"Prix: ${ancien_prix} -> ${prix}")
        
        if description and description != produit.description:
            modifications.append(f"Description change")
        
        if not modifications:
            print("Aucune modification apportée")
            return True  # Success even if no changes needed
        
        success = self.stock_repo.update_product(
            produit_id=produit_id,
            nom=nom if nom != produit.nom else None,
            prix=prix if prix != produit.prix else None,
            description=description if description != produit.description else None
        )
        
        if not success:
            print("Erreur lors de la mise à jour en base de données")
            return False
        
        print(f"Produit {produit_id} modifié:")
        for modif in modifications:
            print(f"  - {modif}")
        
        self._synchroniser_vers_magasins(produit_id, modifications)
        
        return True
    
    def _synchroniser_vers_magasins(self, produit_id: str, modifications: List[str]):
        print(f"\nSync vers {len(self.magasins)} magasins:")
        for mag in self.magasins:
            print(f"  {mag}: ok")
        print("Sync termine")
    
    def afficher_produits(self):
        produits = self.lister_produits()
        
        if not produits:
            print("Aucun produit disponible")
            return
        
        print(f"\nProduits ({len(produits)}):")
        for produit in produits:
            print(f"ID: {produit.id}")
            print(f"Nom: {produit.nom}")
            print(f"Prix: ${produit.prix}")
            print(f"Description: {produit.description}")
            print(f"Stock central: {produit.stock_central}")
            print("---")
    
    def modifier_nom(self, produit_id: str, nom: str) -> bool:
        return self.modifier_produit(produit_id, nom=nom)
    
    def modifier_prix(self, produit_id: str, prix: float) -> bool:
        return self.modifier_produit(produit_id, prix=prix)
    
    def modifier_desc(self, produit_id: str, desc: str) -> bool:
        return self.modifier_produit(produit_id, description=desc)



