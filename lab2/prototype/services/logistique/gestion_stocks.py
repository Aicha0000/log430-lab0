"""
Service de gestion des stocks - Centre logistique
UC2: Consultation du stock central par les magasins
"""
from typing import List, Optional
import uuid
from datetime import datetime

# Import des modèles et repositories
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from commun.modeles.produit import Produit, DemandeReapprovisionnement
from commun.repositories.stock_repository import StockRepository


class StockCentralRepository(StockRepository):
    """Implémentation concrète - Repository pour stock central (PostgreSQL)"""
    
    def __init__(self):
        # Simulation de données pour prototype
        # En production : connexion PostgreSQL
        self._produits = self._init_data_prototype()
        self._demandes = []
    
    def _init_data_prototype(self) -> dict:
        """Données de test pour le prototype - Boissons"""
        return {
            "1": Produit(
                id="1",
                nom="Coca-Cola",
                description="Boisson gazeuse classique en canette",
                prix=1.99,
                stock_central=150,
                seuil_critique=10
            ),
            "2": Produit(
                id="2", 
                nom="Snapple",
                description="Jus de pomme naturel Snapple",
                prix=2.49,
                stock_central=8,  # Stock faible
                seuil_critique=10
            ),
            "3": Produit(
                id="3",
                nom="Jus d'Orange Tropicana",
                description="Jus d'orange",
                prix=4.99,
                stock_central=45,
                seuil_critique=10
            ),
            "4": Produit(
                id="4",
                nom="Sprite",
                description="Boisson gazeuse citron-lime",
                prix=1.99,
                stock_central=120,
                seuil_critique=10
            ),
            "5": Produit(
                id="5",
                nom="Frutopia",
                description="Boisson aux fruits",
                prix=2.79,
                stock_central=5,  # Stock très faible !
                seuil_critique=10
            ),
            "6": Produit(
                id="6",
                nom="Jus de Pomme Oasis",
                description="Jus de pomme 100% naturel",
                prix=3.99,
                stock_central=35,
                seuil_critique=10
            )
        }
    
    def get_produit_by_id(self, produit_id: str) -> Optional[Produit]:
        """UC2: Consulter un produit spécifique"""
        return self._produits.get(produit_id)
    
    def get_all_produits(self) -> List[Produit]:
        """UC2: Consulter tous les produits"""
        return list(self._produits.values())
    
    def search_produits(self, terme_recherche: str) -> List[Produit]:
        """UC2: Rechercher des produits par nom"""
        terme = terme_recherche.lower()
        return [p for p in self._produits.values() 
                if terme in p.nom.lower() or terme in p.description.lower()]
    
    def get_stock_disponible(self, produit_id: str) -> int:
        """UC2: Stock disponible pour un produit"""
        produit = self.get_produit_by_id(produit_id)
        return produit.stock_central if produit else 0
    
    def create_demande_reapprovisionnement(self, demande: DemandeReapprovisionnement) -> bool:
        """UC2: Créer demande de réapprovisionnement"""
        demande.id = str(uuid.uuid4())
        demande.created_at = datetime.now()
        self._demandes.append(demande)
        return True
    
    def get_produits_low_stock(self, seuil: int = 10) -> List[Produit]:
        """UC7: Produits avec stock faible"""
        return [p for p in self._produits.values() if p.stock_central <= seuil]


class GestionStocks:
    """Service principal de gestion des stocks - UC2"""
    
    def __init__(self, stock_repository: StockRepository):
        self.stock_repo = stock_repository
    
    def consulter_stock_central(self, produit_id: str) -> Optional[Produit]:
        """UC2: Employé magasin consulte stock central"""
        produit = self.stock_repo.get_produit_by_id(produit_id)
        if produit:
            print(f"Stock central - {produit}")
            return produit
        else:
            print(f"Produit {produit_id} non trouvé")
            return None
    
    def rechercher_produits(self, terme: str) -> List[Produit]:
        """UC2: Recherche de produits"""
        produits = self.stock_repo.search_produits(terme)
        print(f" {len(produits)} produit(s) trouvé(s) pour '{terme}'")
        for p in produits:
            status = "STOCK FAIBLE" if p.is_stock_low() else "Stock OK"
            print(f"  - {p} ({status})")
        return produits
    
    def lister_tous_produits(self) -> List[Produit]:
        """UC2: Liste complète des produits"""
        produits = self.stock_repo.get_all_produits()
        print(f" {len(produits)} produits dans le stock central:")
        for p in produits:
            status = "STOCK FAIBLE" if p.is_stock_low() else "Stock OK"
            print(f"  - {p} ({status})")
        return produits
    
    def demander_reapprovisionnement(self, magasin_id: str, produit_id: str, quantite: int) -> bool:
        """UC2: Déclencher demande de réapprovisionnement"""
        produit = self.stock_repo.get_produit_by_id(produit_id)
        
        if not produit:
            print(f"Produit {produit_id} non trouvé")
            return False
        
        if quantite <= 0:
            print(f"Quantité invalide: {quantite}")
            return False
        
        demande = DemandeReapprovisionnement(
            id="",  # Sera généré par le repository
            magasin_id=magasin_id,
            produit_id=produit_id,
            quantite_demandee=quantite
        )
        
        success = self.stock_repo.create_demande_reapprovisionnement(demande)
        return success


# Instance globale pour le prototype
stock_repository = StockCentralRepository()
gestion_stocks = GestionStocks(stock_repository)


def main():
    """Point d'entrée pour tests du service logistique"""
    print("Service Logistique - Gestion des stocks")
    print("=" * 50)
    
    # Test UC2 - Consultation stock
    print("\n Test UC2 - Consultation stock central:")
    gestion_stocks.consulter_stock_central("PROD-001")
    gestion_stocks.consulter_stock_central("PROD-999")  # Inexistant
    
    print("\n Test UC2 - Recherche produits:")
    gestion_stocks.rechercher_produits("laptop")
    
    print("\n Test UC2 - Liste complète:")
    gestion_stocks.lister_tous_produits()
    
    print("\n Test UC2 - Demande réapprovisionnement:")
    gestion_stocks.demander_reapprovisionnement("MAG-001", "PROD-002", 15)


if __name__ == "__main__":
    main()
