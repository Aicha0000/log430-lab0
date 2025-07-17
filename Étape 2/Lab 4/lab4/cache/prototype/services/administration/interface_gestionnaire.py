# UC1 – Générer un rapport consolidé des ventes et UC3 – Visualiser les performances des magasins - par un gestionnaire de la maison mère
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from commun.repositories.instances import rapports_service, produits_service
from services.administration.tableau_bord import tableau_bord_service


class ConsoleGestionnaire:
    
    def __init__(self):
        self.service_rapports = rapports_service
        self.service_produits = produits_service
        self.service_dashboard = tableau_bord_service
    
    def afficher_menu_principal(self):
        print("\nInterface Gestionnaire")
        print("1. Rapport consolide")
        print("2. Rapport magasin")
        print("3. Tableau de bord (UC3)")
        print("4. Gestion produits (UC4)")
        print("5. Magasins performance")
        print("6. Quitter")
    
    def generer_rapport_consolide(self):
        print("\nRapport:")
        
        try:
            jours = input("Jours (30 par defaut): ").strip()
            periode = int(jours) if jours else 30
        except ValueError:
            periode = 30
        
        print(f"Rapport {periode} jours...")
        rapport = self.service_rapports.generer_rapport_consolide(periode)
        self.service_rapports.afficher_rapport_detaille(rapport)
    
    def rapport_par_magasin(self):
        print("\nRAPPORT PAR MAGASIN")
        magasins_disponibles = ["magasin 1", "magasin 2", "magasin 3", "magasin 4", "magasin 5"]
        
        print("Magasins disponibles:")
        for i, mag in enumerate(magasins_disponibles, 1):
            print(f"{i}. {mag}")
        
        try:
            choix = input("Numero: ").strip()
            
            if choix.isdigit() and 1 <= int(choix) <= len(magasins_disponibles):
                magasin_id = magasins_disponibles[int(choix) - 1]
            else:
                print("Choix invalide")
                return
            
            self.service_rapports.generer_rapport_par_magasin(magasin_id)
            
        except Exception as e:
            print(f"Erreur: {e}")
    
    def afficher_tableau_bord(self):
        print("\nTABLEAU DE BORD (UC3)")
        print("Generation du tableau de bord...")
        dashboard = self.service_dashboard.generer_tableau_bord()
        self.service_dashboard.afficher_tableau_bord(dashboard)
    
    def gerer_produits(self):
        print("\nGESTION PRODUITS (UC4)")
        
        while True:
            print("\nOptions:")
            print("1. Lister tous les produits")
            print("2. Modifier un produit")
            print("3. Modifier nom seulement")
            print("4. Modifier prix seulement")
            print("5. Modifier description seulement")
            print("6. Retour")
            
            choix = input("Choix (1-6): ").strip()
            
            if choix == "1":
                self.service_produits.afficher_produits()
            elif choix == "2":
                self.modifier_produit_complet()
            elif choix == "3":
                self.modifier_nom_seulement()
            elif choix == "4":
                self.modifier_prix_seulement()
            elif choix == "5":
                self.modifier_description_seulement()
            elif choix == "6":
                break
            else:
                print("Choix invalide (1-6)")
            
            input("\nAppuyez sur Entree pour continuer...")
    
    def modifier_produit_complet(self):
        print("\nMODIFICATION PRODUIT COMPLETE")
        
        produits = self.service_produits.lister_produits()
        if not produits:
            print("Aucun produit disponible")
            return
        
        print("\nProduits disponibles:")
        for produit in produits:
            print(f"{produit.id}. {produit.nom} - ${produit.prix}")
        
        produit_id = input("\nID du produit a modifier: ").strip()
        produit = self.service_produits.obtenir_produit(produit_id)
        
        if not produit:
            print("Produit non trouve")
            return
        
        print(f"\nProduit selectionne: {produit.nom}")
        print(f"Prix actuel: ${produit.prix}")
        print(f"Description actuelle: {produit.description}")
        
        nouveau_nom = input(f"\nNouveau nom (actuel: {produit.nom}): ").strip()
        nouveau_nom = nouveau_nom if nouveau_nom else None
        
        nouveau_prix_str = input(f"Nouveau prix (actuel: ${produit.prix}): ").strip()
        nouveau_prix = None
        if nouveau_prix_str:
            try:
                nouveau_prix = float(nouveau_prix_str)
            except ValueError:
                print("Prix invalide, ignore")
        
        nouvelle_description = input(f"Nouvelle description: ").strip()
        nouvelle_description = nouvelle_description if nouvelle_description else None
        
        success = self.service_produits.modifier_produit(
            produit_id, nouveau_nom, nouveau_prix, nouvelle_description
        )
        
        if not success:
            print("Echec de la modification")
    
    def modifier_nom_seulement(self):
        print("\nMODIFICATION NOM PRODUIT")
        
        produits = self.service_produits.lister_produits()
        print("\nProduits disponibles:")
        for produit in produits:
            print(f"{produit.id}. {produit.nom}")
        
        produit_id = input("\nID du produit: ").strip()
        produit = self.service_produits.obtenir_produit(produit_id)
        
        if not produit:
            print("Produit non trouve")
            return
        
        print(f"Nom actuel: {produit.nom}")
        nouveau_nom = input("Nouveau nom: ").strip()
        
        if not nouveau_nom:
            print("Nom requis")
            return
        
        self.service_produits.modifier_produit(produit_id, nom=nouveau_nom)
    
    def modifier_prix_seulement(self):
        print("\nMODIFICATION PRIX PRODUIT")
        
        produits = self.service_produits.lister_produits()
        print("\nProduits disponibles:")
        for produit in produits:
            print(f"{produit.id}. {produit.nom} - ${produit.prix}")
        
        produit_id = input("\nID du produit: ").strip()
        produit = self.service_produits.obtenir_produit(produit_id)
        
        if not produit:
            print("Produit non trouve")
            return
        
        print(f"Prix actuel: ${produit.prix}")
        
        try:
            nouveau_prix = float(input("Nouveau prix: ").strip())
            self.service_produits.modifier_produit(produit_id, prix=nouveau_prix)
        except ValueError:
            print("Prix invalide")
    
    def modifier_description_seulement(self):
        print("\nMODIFICATION DESCRIPTION PRODUIT")
        
        produits = self.service_produits.lister_produits()
        print("\nProduits disponibles:")
        for produit in produits:
            print(f"{produit.id}. {produit.nom}")
        
        produit_id = input("\nID du produit: ").strip()
        produit = self.service_produits.obtenir_produit(produit_id)
        
        if not produit:
            print("Produit non trouve")
            return
        
        print(f"Description actuelle: {produit.description}")
        nouvelle_description = input("Nouvelle description: ").strip()
        
        if not nouvelle_description:
            print("Description requise")
            return
        
        self.service_produits.modifier_produit(produit_id, description=nouvelle_description)
    
    def lister_magasins(self):
        print("\nPERFORMANCE MAGASINS")
        
        rapport = self.service_rapports.generer_rapport_consolide(30)
        
        magasins_tries = sorted(
            rapport.ventes_par_magasin.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        for i, (magasin, total) in enumerate(magasins_tries, 1):
            print(f"{i}. {magasin}: ${total:.2f}")
        
        print(f"\nTotal reseau: ${rapport.total_general:.2f}")
    
    def run(self):
        print("Interface gestionnaire maison mere")
        
        while True:
            self.afficher_menu_principal()
            
            try:
                choix = input("Choix (1-6): ").strip()
                
                if choix == "1":
                    self.generer_rapport_consolide()
                elif choix == "2":
                    self.rapport_par_magasin()
                elif choix == "3":
                    self.afficher_tableau_bord()
                elif choix == "4":
                    self.gerer_produits()
                elif choix == "5":
                    self.lister_magasins()
                elif choix == "6":
                    print("Au revoir!")
                    break
                else:
                    print("Choix invalide (1-6)")
                
                input("\nAppuyez sur Entree pour continuer...")
                
            except KeyboardInterrupt:
                print("\nFermeture...")
                break
            except Exception as e:
                print(f"Erreur: {e}")

def main():
    console = ConsoleGestionnaire()
    console.run()

if __name__ == "__main__":
    main()
