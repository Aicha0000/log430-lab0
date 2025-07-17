"""
Interface principale centre logistique
UC2: Gestion des stocks centraux
UC6: Reapprovisionnement des magasins
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from commun.repositories.instances import gestion_stocks, reappro_service


class InterfaceLogistique:
    """Interface principale centre logistique - UC2 et UC6"""
    
    def __init__(self):
        self.service_stocks = gestion_stocks
        self.service_reappro = reappro_service
    
    def afficher_menu_principal(self):
        print(f"\nCENTRE LOGISTIQUE - Interface Principale")
        print("=" * 45)
        print("1. Consulter stock central (UC2)")
        print("2. Rechercher produits (UC2)")
        print("3. Voir tous les produits (UC2)")
        print("4. Reapprovisionnement (UC6)")
        print("5. Quitter")
        print("-" * 45)
    
    def consulter_stock_central(self):
        print("\nCONSULTATION STOCK CENTRAL")
        
        produits = self.service_stocks.lister_tous_produits()
        print("\nProduits disponibles:")
        for produit in produits[:5]:
            print(f"{produit.id}. {produit.nom} - Stock: {produit.stock_central}")
        
        produit_id = input("\nID du produit a consulter: ").strip()
        
        if produit_id:
            self.service_stocks.consulter_stock_central(produit_id)
    
    def rechercher_produits(self):
        print("\nRECHERCHE PRODUITS")
        
        terme = input("Terme de recherche: ").strip()
        
        if terme:
            self.service_stocks.rechercher_produits(terme)
        else:
            print("Terme de recherche REQUIS")
    
    def voir_tous_produits(self):
        print("\nTOUS LES PRODUITS DU STOCK CENTRAL")
        self.service_stocks.lister_tous_produits()
    
    def gerer_reapprovisionnement(self):
        print("\nREAPPROVISIONNEMENT (UC6)")
        
        while True:
            print("\nOptions:")
            print("1. Voir demandes en attente")
            print("2. Approuver et traiter demande")
            print("3. Rejeter demande")
            print("4. Voir stocks magasin")
            print("5. Retour")
            
            choix = input("Choix (1-5): ").strip()
            
            if choix == "1":
                self.voir_demandes_en_attente()
            elif choix == "2":
                self.approuver_et_traiter_demande()
            elif choix == "3":
                self.rejeter_demande()
            elif choix == "4":
                self.voir_stock_magasin()
            elif choix == "5":
                break
            else:
                print("Choix invalide (1-5)")
            
            input("\nAppuyez sur Entree pour continuer...")
    
    def voir_demandes_en_attente(self):
        print("\nDEMANDES EN ATTENTE")
        self.service_reappro.afficher_demandes_en_attente()
    
    def approuver_et_traiter_demande(self):
        print("\nAPPROUVER ET TRAITER DEMANDE")
        
        demandes = self.service_reappro.lister_demandes_en_attente()
        if not demandes:
            print("Aucune demande en attente")
            return
        
        print("\nDemandes en attente:")
        for i, demande in enumerate(demandes, 1):
            produit = self.service_stocks.stock_repo.get_produit_by_id(demande.produit_id)
            produit_nom = produit.nom if produit else "Produit inconnu"
            print(f"{i}. {demande.id} - {demande.magasin_id} - {produit_nom} - Qtte: {demande.quantite_demandee}")
        
        try:
            choix = int(input(f"\nChoisir demande (1-{len(demandes)}): ").strip())
            if 1 <= choix <= len(demandes):
                demande_selectionnee = demandes[choix - 1]
            else:
                print("Choix invalide")
                return
        except ValueError:
            print("Entree invalide")
            return
        
        success = self.service_reappro.approuver_et_traiter(demande_selectionnee.id)
        if success:
            print("Demande approuvee et traitee avec succes")
        else:
            print("Echec - Verifiez le stock disponible")
    
    def rejeter_demande(self):
        print("\nREJET DEMANDE")
        
        demandes = self.service_reappro.lister_demandes_en_attente()
        if not demandes:
            print("Aucune demande en attente")
            return
        
        print("\nDemandes en attente:")
        for i, demande in enumerate(demandes, 1):
            produit = self.service_stocks.stock_repo.get_produit_by_id(demande.produit_id)
            produit_nom = produit.nom if produit else "Produit inconnu"
            print(f"{i}. {demande.id} - {demande.magasin_id} - {produit_nom}")
        
        try:
            choix = int(input(f"\nChoisir demande a rejeter (1-{len(demandes)}): ").strip())
            if 1 <= choix <= len(demandes):
                demande_selectionnee = demandes[choix - 1]
            else:
                print("Choix invalide")
                return
        except ValueError:
            print("Entree invalide")
            return
        
        motif = input("Motif de rejet: ").strip()
        success = self.service_reappro.rejeter_demande(demande_selectionnee.id, motif)
        if success:
            print("Demande rejetee")
    
    def voir_stock_magasin(self):
        print("\nSTOCK MAGASIN")
        
        magasins = ["magasin 1", "magasin 2", "magasin 3", "magasin 4", "magasin 5"]
        
        print("\nMagasins disponibles:")
        for i, magasin in enumerate(magasins, 1):
            print(f"{i}. {magasin}")
        
        try:
            choix = int(input(f"\nChoisir magasin (1-{len(magasins)}): ").strip())
            if 1 <= choix <= len(magasins):
                magasin_id = magasins[choix - 1]
                self.service_reappro.afficher_stock_magasin(magasin_id)
            else:
                print("Choix invalide")
        except ValueError:
            print("Entree invalide")
    
    def run(self):
        print("Interface centre logistique")
        
        while True:
            self.afficher_menu_principal()
            
            try:
                choix = input("Choix (1-5): ").strip()
                
                if choix == "1":
                    self.consulter_stock_central()
                elif choix == "2":
                    self.rechercher_produits()
                elif choix == "3":
                    self.voir_tous_produits()
                elif choix == "4":
                    self.gerer_reapprovisionnement()
                elif choix == "5":
                    print("Au revoir!")
                    break
                else:
                    print("Choix invalide (1-5)")
                
                input("\nAppuyez sur Entree pour continuer...")
                
            except KeyboardInterrupt:
                print("\nFermeture...")
                break
            except Exception as e:
                print(f"Erreur: {e}")


def main():
    interface = InterfaceLogistique()
    interface.run()


if __name__ == "__main__":
    main()
