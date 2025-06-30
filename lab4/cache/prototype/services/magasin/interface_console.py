
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from commun.modeles.produit import Produit, DemandeReapprovisionnement
from typing import List, Optional
from datetime import datetime


class ConsoleEmployeMagasin:
    
    def __init__(self, magasin_id: str = "MAGASIN"):
        self.magasin_id = magasin_id
        from commun.repositories.instances import gestion_stocks
        self.service_logistique = gestion_stocks
    
    def afficher_menu_principal(self):
        print(f"\nMagasin {self.magasin_id}")
        print("1. Stock")
        print("2. Recherche")
        print("3. Tous produits")
        print("4. Reappro")
        print("5. Quitter")
    
    def consulter_stock_produit(self):
        print("\nStock:")
        produit_id = input("ID du produit: ").strip()
        
        produit = self.service_logistique.get_stock(produit_id)
        
        if produit:
            print(f"{produit.nom} - Stock: {produit.stock_central}")
            
            if produit.is_stock_low():
                print(f"Stock faible (seuil: {produit.seuil_critique})")
                if input("Demander reappro? (o/n): ").lower() == 'o':
                    self.demander_reapprovisionnement_produit(produit.id)
        else:
            print(f"Produit {produit_id} non trouve")
    
    def rechercher_produits(self):
        print("\nRecherche:")
        terme = input("Terme de recherche: ").strip()
        
        produits = self.service_logistique.search(terme)
        
        if produits:
            for i, p in enumerate(produits, 1):
                status = "Faible stock" if p.is_stock_low() else "stock ok"
                print(f"{i}. {p.nom} (ID: {p.id}) - Stock: {p.stock_central} {status}")
            
            choix = input("Reappro pour quel produit? (numero ou 'n'): ")
            if choix.isdigit() and 1 <= int(choix) <= len(produits):
                produit_choisi = produits[int(choix) - 1]
                self.demander_reapprovisionnement_produit(produit_choisi.id)
    
    def lister_tous_produits(self):
        print("\nProduits:")
        produits = self.service_logistique.list_all()
        
        for p in produits:
            status = "FAIBLE" if p.is_stock_low() else "Stock OK"
            print(f"{p.nom} (ID: {p.id}) - Stock: {p.stock_central} - {status}")
    
    def demander_reapprovisionnement_produit(self, produit_id: str = None):
        print("\nReappro:")
        
        if not produit_id:
            produit_id = input("ID du produit: ").strip()
        
        produit = self.service_logistique.get_stock(produit_id)
        if not produit:
            print(f"Produit {produit_id} non trouve")
            return
        
        print(f"Produit: {produit.nom} - Stock actuel: {produit.stock_central}")
        
        try:
            quantite = int(input("Quantite a commander: "))
            
            if quantite <= 0:
                print("Quantite invalide")
                return
            
            demande = DemandeReapprovisionnement(
                id="",  # Sera assigné par le repository
                magasin_id=self.magasin_id,
                produit_id=produit_id,
                quantite_demandee=quantite,
                created_at=datetime.now()
            )
            
            success = self.service_logistique.stock_repo.create_demande_reapprovisionnement(demande)
            
            if success:
                print(f"Demande envoyee: {quantite}x {produit.nom}")
            else:
                print("Erreur lors de la demande")
                
        except ValueError:
            print("Quantite invalide")
    
    def run(self):
        print("Console employe magasin")
        
        while True:
            self.afficher_menu_principal()
            
            try:
                choix = input("Choix (1-5): ").strip()
                
                if choix == "1":
                    self.consulter_stock_produit()
                elif choix == "2":
                    self.rechercher_produits()
                elif choix == "3":
                    self.lister_tous_produits()
                elif choix == "4":
                    self.demander_reapprovisionnement_produit()
                elif choix == "5":
                    print("Bye!")
                    break
                else:
                    print("Choix invalide (1-5)")
                
                input("\nAppuyez sur Entree pour continuer...")
                
            except KeyboardInterrupt:
                print("\n Fermeture...")
                break
            except Exception as e:
                print(f"Erreur: {e}")


def main():
    console = ConsoleEmployeMagasin("MAGASIN 1")
    console.run()


if __name__ == "__main__":
    main()
