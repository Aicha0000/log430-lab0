"""
UC6 – Approvisionner un magasin depuis le centre logistique
"""
from typing import List, Optional, Dict
from datetime import datetime

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from commun.modeles.produit import Produit, DemandeReapprovisionnement
from commun.repositories.stock_repository import StockRepository


class ReapprovisionnementService:
    
    def __init__(self, stock_repository: StockRepository):
        self.stock_repo = stock_repository
        # Simulation des stocks par magasin (ID magasin -> ID produit -> quantité)
        self.stocks_magasins = self._init_stocks_magasins()
    
    def _init_stocks_magasins(self) -> Dict[str, Dict[str, int]]:
        magasins = ["magasin 1", "magasin 2", "magasin 3", "magasin 4", "magasin 5"]
        stocks = {}
        
        for magasin in magasins:
            stocks[magasin] = {
                "1": 15,  # Coca-Cola
                "2": 3,   # Snapple
                "3": 20,  # Jus Orange
                "4": 18,  # Sprite
                "5": 2    # Frutopia
            }
        
        return stocks
    
    def lister_demandes_en_attente(self) -> List[DemandeReapprovisionnement]:
        toutes_demandes = self.stock_repo.get_demandes_reapprovisionnement()
        return [d for d in toutes_demandes if d.statut == "EN_ATTENTE"]
    
    def obtenir_demande(self, demande_id: str) -> Optional[DemandeReapprovisionnement]:
        toutes_demandes = self.stock_repo.get_demandes_reapprovisionnement()
        for demande in toutes_demandes:
            if demande.id == demande_id:
                return demande
        return None
    
    def valider_demande(self, demande_id: str, approuve: bool, motif: str = "") -> bool:
        demande = self.obtenir_demande(demande_id)
        
        if not demande:
            print(f"Demande {demande_id} non trouvée")
            return False
        
        if demande.statut != "EN_ATTENTE":
            print(f"Demande {demande_id} déjà traitée (statut: {demande.statut})")
            return False
        
        if approuve:
            produit = self.stock_repo.get_produit_by_id(demande.produit_id)
            if not produit:
                print(f"Produit {demande.produit_id} non trouvé")
                return False
            
            if produit.stock_central < demande.quantite_demandee:
                print(f"Stock insuffisant: {produit.stock_central} < {demande.quantite_demandee}")
                self.stock_repo.update_demande_statut(demande_id, "REJETE")
                print(f"Demande {demande_id} REJETÉE - Stock insuffisant")
                return False
            
            self.stock_repo.update_demande_statut(demande_id, "APPROUVE")
            print(f"Demande {demande_id} APPROUVÉE")
            print(f"  Magasin: {demande.magasin_id}")
            print(f"  Produit: {produit.nom}")
            print(f"  Quantité: {demande.quantite_demandee}")
            
        else:
            self.stock_repo.update_demande_statut(demande_id, "REJETE")
            print(f"Demande {demande_id} REJETÉE")
            if motif:
                print(f"  Motif: {motif}")
        
        return True
    
    def traiter_reapprovisionnement(self, demande_id: str) -> bool:
        demande = self.obtenir_demande(demande_id)
        
        if not demande:
            print(f"Demande {demande_id} non trouvée")
            return False
        
        if demande.statut != "APPROUVE":
            print(f"Demande {demande_id} non approuvée (statut: {demande.statut})")
            return False
        
        produit = self.stock_repo.get_produit_by_id(demande.produit_id)
        if not produit:
            print(f"Produit {demande.produit_id} non trouvé")
            return False
        
        # Vérifier encore le stock central avant le transfert
        if produit.stock_central < demande.quantite_demandee:
            print(f"Stock central insuffisant: {produit.stock_central} < {demande.quantite_demandee}")
            return False
        
        print(f"\nTRANSFERT DE STOCK - Demande {demande_id}")
        print(f"Produit: {produit.nom}")
        print(f"Quantité transférée: {demande.quantite_demandee}")
        
        stock_avant_central = produit.stock_central
        nouvelle_quantite = produit.stock_central - demande.quantite_demandee
        self.stock_repo.update_stock(demande.produit_id, nouvelle_quantite)
        print(f"Stock central: {stock_avant_central} -> {nouvelle_quantite}")
        
        stock_avant_magasin = self.stocks_magasins[demande.magasin_id][demande.produit_id]
        self.stocks_magasins[demande.magasin_id][demande.produit_id] += demande.quantite_demandee
        stock_apres_magasin = self.stocks_magasins[demande.magasin_id][demande.produit_id]
        print(f"Stock {demande.magasin_id}: {stock_avant_magasin} -> {stock_apres_magasin}")
        
        self.stock_repo.update_demande_statut(demande_id, "TRAITE")
        
        print(f"Transfert terminé - Demande {demande_id} TRAITÉE")
        
        return True
    
    def approuver_et_traiter(self, demande_id: str) -> bool:
        success_validation = self.valider_demande(demande_id, True)
        if not success_validation:
            return False
        
        return self.traiter_reapprovisionnement(demande_id)
    
    def rejeter_demande(self, demande_id: str, motif: str = "") -> bool:
        return self.valider_demande(demande_id, False, motif)
    
    def afficher_demandes_en_attente(self):
        demandes = self.lister_demandes_en_attente()
        
        if not demandes:
            print("Aucune demande en attente")
            return
        
        print(f"\nDEMANDES EN ATTENTE ({len(demandes)}):")
        print("-" * 60)
        
        for demande in demandes:
            produit = self.stock_repo.get_produit_by_id(demande.produit_id)
            produit_nom = produit.nom if produit else "Produit inconnu"
            stock_disponible = produit.stock_central if produit else 0
            
            print(f"ID: {demande.id}")
            print(f"Magasin: {demande.magasin_id}")
            print(f"Produit: {produit_nom} (ID: {demande.produit_id})")
            print(f"Quantité demandée: {demande.quantite_demandee}")
            print(f"Stock central disponible: {stock_disponible}")
            
            if stock_disponible >= demande.quantite_demandee:
                print("Statut: TRAITABLE")
            else:
                print("Statut: STOCK INSUFFISANT")
            
            print("-" * 60)
    
    def afficher_stock_magasin(self, magasin_id: str):
        if magasin_id not in self.stocks_magasins:
            print(f"Magasin {magasin_id} non trouvé")
            return
        
        stocks = self.stocks_magasins[magasin_id]
        print(f"\nSTOCK MAGASIN {magasin_id}:")
        print("-" * 40)
        
        for produit_id, quantite in stocks.items():
            produit = self.stock_repo.get_produit_by_id(produit_id)
            nom_produit = produit.nom if produit else f"Produit {produit_id}"
            print(f"{nom_produit}: {quantite} unités")


