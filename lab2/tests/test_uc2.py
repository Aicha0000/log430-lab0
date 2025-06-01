#!/usr/bin/env python3
"""
Test simple de UC2 - Consulter stock central et déclencher réapprovisionnement
"""
import sys
import os

# Ajouter le chemin du prototype
prototype_path = os.path.join(os.path.dirname(__file__), '..', 'prototype')
sys.path.append(prototype_path)

def test_uc2_consultation_stock():
    """Test UC2: Consultation du stock central"""
    print("TEST UC2 - Consultation stock central")
    print("=" * 50)
    
    # Import du service logistique
    from services.logistique.gestion_stocks import gestion_stocks
    
    # Test 1: Consulter un produit existant
    print("\n Test 1: Consultation produit existant")
    produit = gestion_stocks.consulter_stock_central("DRINK-001")
    assert produit is not None, "Produit DRINK-001 devrait exister"
    assert produit.nom == "Coca-Cola 355ml", "Nom du produit incorrect"
    print(f"Résultat: {produit}")
    
    # Test 2: Consulter un produit inexistant
    print("\n Test 2: Consultation produit inexistant")
    produit = gestion_stocks.consulter_stock_central("DRINK-999")
    assert produit is None, "Produit DRINK-999 ne devrait pas exister"
    print("Résultat: Produit non trouvé (attendu)")
    
    # Test 3: Recherche de produits
    print("\n Test 3: Recherche de produits")
    produits = gestion_stocks.rechercher_produits("coca")
    assert len(produits) > 0, "Devrait trouver au moins un Coca"
    print(f"Résultat: {len(produits)} produit(s) trouvé(s)")
    
    # Test 4: Demande de réapprovisionnement
    print("\n Test 4: Demande de réapprovisionnement")
    success = gestion_stocks.demander_reapprovisionnement("MAG-001", "DRINK-002", 20)
    assert success, "La demande devrait être créée avec succès"
    print("Résultat: Demande créée avec succès")
    
    print("\n Tous les tests UC2 sont PASSÉS!")

def test_interface_console_simulation():
    """Simulation de l'interface console (sans interaction utilisateur)"""
    print("\n TEST INTERFACE CONSOLE - Simulation")
    print("=" * 50)
    
    from services.magasin.interface_console import ConsoleEmployeMagasin
    
    console = ConsoleEmployeMagasin("MAG-TEST")
    
    # Test méthodes de base
    print("\n Test: Consultation stock via console")
    produit = console.service_logistique.consulter_stock_central("DRINK-001")
    assert produit is not None
    
    print("\n Test: Recherche via console")
    produits = console.service_logistique.rechercher_produits("jus")
    assert len(produits) > 0
    
    print("\n Test: Demande réappro via console")
    success = console.service_logistique.demander_reapprovisionnement("MAG-TEST", "DRINK-003", 10)
    assert success
    
    print("\n Tests interface console PASSÉS!")

def demo_uc2():
    """Démonstration complète de UC2"""
    print("\n DÉMONSTRATION UC2 - Scénario complet")
    print("=" * 60)
    
    from services.logistique.gestion_stocks import gestion_stocks
    
    print("\n Scénario: Employé consulte stock + fait demande réapprovisionnement")
    print("-" * 60)
    
    # 1. Employé cherche un produit
    print("Employé recherche 'snapple':")
    produits = gestion_stocks.rechercher_produits("snapple")
    
    # 2. Il consulte le stock d'un produit spécifique
    print("\n Employé consulte stock de DRINK-002 (Snapple):")
    produit = gestion_stocks.consulter_stock_central("DRINK-002")
    
    # 3. Il voit que le stock est faible et fait une demande
    if produit and produit.is_stock_low():
        print("\n Stock faible détecté! Demande de réapprovisionnement:")
        success = gestion_stocks.demander_reapprovisionnement("MAG-001", "DRINK-002", 25)
        if success:
            print("Demande envoyée au centre logistique!")
    
    print("\n Scénario UC2 terminé avec succès!")

def main():
    """Tests complets UC2"""
    print("TESTS UC2 - Consultation stock central + réapprovisionnement")
    print("=" * 70)
    
    try:
        # Tests unitaires
        test_uc2_consultation_stock()
        
        # Tests interface
        test_interface_console_simulation()
        
        # Démo complète
        demo_uc2()
        
        print("\n" + "=" * 70)
        print("TOUS LES TESTS UC2 RÉUSSIS!")
        print("Repository Pattern: Fonctionnel")
        print("Service Logistique: Fonctionnel") 
        print("Interface Console: Fonctionnelle")
        print("Communication inter-services: OK")
        print("\n UC2 est prêt pour utilisation!")
        
    except Exception as e:
        print(f"\nERREUR dans les tests: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
