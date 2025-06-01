"""
Interface console SIMPLIFIÉE pour employés de magasin
UC2: Consulter le stock central et déclencher un réapprovisionnement
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from commun.modeles.produit import Produit
from typing import List, Optional


class ConsoleEmployeMagasin:
    """Interface console pour employé de magasin - UC2"""
    
    def __init__(self, magasin_id: str = "MAG-001"):
        self.magasin_id = magasin_id
        from services.logistique.gestion_stocks import gestion_stocks
        self.service_logistique = gestion_stocks
    
    def afficher_menu_principal(self):
        """Menu principal de l'interface console"""
        print(f"\n MAGASIN {self.magasin_id}")
        print("=" * 30)
        print("1. Consulter stock central")
        print("2. Rechercher produits")
        print("3. Voir tous les produits")
        print("4. Demander réapprovisionnement")
        print("5. Quitter")
        print("-" * 30)
    
    def consulter_stock_produit(self):
        """UC2: Consulter stock central d'un produit spécifique"""
        print("\n CONSULTATION STOCK")
        produit_id = input("ID du produit: ").strip()
        
        produit = self.service_logistique.consulter_stock_central(produit_id)
        
        if produit:
            print(f"{produit.nom} - Stock: {produit.stock_central}")
            
            if produit.is_stock_low():
                print(f"Stock faible (seuil: {produit.seuil_critique})")
                if input("Demander réappro? (o/n): ").lower() == 'o':
                    self.demander_reapprovisionnement_produit(produit.id)
        else:
            print(f"Produit {produit_id} non trouvé")
    
    def rechercher_produits(self):
        """UC2: Rechercher des produits par nom"""
        print("\n RECHERCHE")
        terme = input("Terme de recherche: ").strip()
        
        produits = self.service_logistique.rechercher_produits(terme)
        
        if produits:
            for i, p in enumerate(produits, 1):
                status = "Faible stock" if p.is_stock_low() else "stock ok"
                print(f"{i}. {p.nom} (ID: {p.id}) - Stock: {p.stock_central} {status}")
            
            choix = input("Réappro pour quel produit? (numéro ou 'n'): ")
            if choix.isdigit() and 1 <= int(choix) <= len(produits):
                produit_choisi = produits[int(choix) - 1]
                self.demander_reapprovisionnement_produit(produit_choisi.id)
    
    def lister_tous_produits(self):
        """UC2: Afficher tous les produits disponibles"""
        print("\nTOUS LES PRODUITS")
        produits = self.service_logistique.lister_tous_produits()
        
        for p in produits:
            status = "FAIBLE" if p.is_stock_low() else "Stock OK"
            print(f"{p.nom} (ID: {p.id}) - Stock: {p.stock_central} - {status}")
    
    def demander_reapprovisionnement_produit(self, produit_id: str = None):
        """UC2: Déclencher une demande de réapprovisionnement"""
        print("\n DEMANDE RÉAPPROVISIONNEMENT")
        
        if not produit_id:
            produit_id = input("ID du produit: ").strip()
        
        produit = self.service_logistique.consulter_stock_central(produit_id)
        if not produit:
            print(f"Produit {produit_id} non trouvé")
            return
        
        print(f"Produit: {produit.nom} - Stock actuel: {produit.stock_central}")
        
        try:
            quantite = int(input("Quantité à commander: "))
            
            if quantite <= 0:
                print("Quantité invalide")
                return
            
            success = self.service_logistique.demander_reapprovisionnement(
                self.magasin_id, produit_id, quantite
            )
            
            if success:
                print(f"Demande envoyée: {quantite}x {produit.nom}")
            else:
                print("Erreur lors de la demande")
                
        except ValueError:
            print("Quantité invalide")
    
    def run(self):
        """Boucle principale de l'interface console"""
        print("Console employé magasin")
        
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
                    print("Au revoir!")
                    break
                else:
                    print("Choix invalide (1-5)")
                
                input("\n⏸  Appuyez sur Entrée pour continuer...")
                
            except KeyboardInterrupt:
                print("\n Fermeture...")
                break
            except Exception as e:
                print(f"Erreur: {e}")


def main():
    """Point d'entrée simplifié"""
    console = ConsoleEmployeMagasin("MAG-001")
    console.run()


if __name__ == "__main__":
    main()
