
from typing import List, Dict
from datetime import datetime, timedelta

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from commun.modeles.vente import Vente, RapportVente
from commun.repositories.vente_repository import VenteRepository


class RapportsConsolides:
    
    def __init__(self, vente_repository: VenteRepository):
        self.vente_repo = vente_repository
    
    def generer_rapport_consolide(self, jours: int = 30) -> RapportVente:
        date_fin = datetime.now()
        date_debut = date_fin - timedelta(days=jours)
        
        ventes_periode = self.vente_repo.get_ventes_by_periode(date_debut, date_fin)
        ventes_magasin = self.vente_repo.get_total_ventes_par_magasin()
        top_produits = self.vente_repo.get_produits_plus_vendus(5)
        
        from commun.repositories.instances import stock_repo
        stocks = {}
        produits = stock_repo.get_all_produits()
        for p in produits:
            stocks[p.id] = {"nom": p.nom, "stock": p.stock_central}
        
        total = sum(ventes_magasin.values())
        
        rapport = RapportVente(
            periode=f"{jours} derniers jours",
            ventes_par_magasin=ventes_magasin,
            produits_plus_vendus=top_produits,
            stocks_restants=stocks,
            total_general=total
        )
        
        return rapport
    
    def afficher_rapport_detaille(self, rapport: RapportVente):
        print(f"\nRAPPORT CONSOLIDE - {rapport.periode}")
        print("=" * 40)
        
        print("\nVENTES PAR MAGASIN:")
        for magasin, total in rapport.ventes_par_magasin.items():
            print(f"{magasin}: ${total:.2f}")
        
        print(f"\nTOP PRODUITS VENDUS:")
        for produit_id, quantite in rapport.produits_plus_vendus:
            nom_produit = rapport.stocks_restants.get(produit_id, {}).get("nom", f"Produit {produit_id}")
            print(f"{nom_produit}: {quantite} unités")
        
        print(f"\nSTOCKS ACTUELS:")
        for produit_id, info in rapport.stocks_restants.items():
            status = "FAIBLE" if info["stock"] <= 10 else "OK"
            print(f"{info['nom']}: {info['stock']} ({status})")
        
        print(f"\nTOTAL: ${rapport.total_general:.2f}")
    
    def generer_rapport_par_magasin(self, magasin_id: str):
        ventes_magasin = self.vente_repo.get_ventes_by_magasin(magasin_id)
        
        if not ventes_magasin:
            print(f"Aucune vente pour {magasin_id}")
            return
        
        total_magasin = sum(v.total for v in ventes_magasin)
        nb_ventes = len(ventes_magasin)
        
        print(f"\nRAPPORT {magasin_id}")
        print(f"Ventes: {nb_ventes}")
        print(f"Total: ${total_magasin:.2f}")
        print(f"Moyenne: ${total_magasin/nb_ventes:.2f}")

