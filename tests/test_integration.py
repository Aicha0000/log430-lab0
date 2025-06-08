#!/usr/bin/env python3
"""
Tests Integration - Lab 2
Tests des interactions entre services et components
"""
import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'prototype'))

from commun.repositories.instances import gestion_stocks
from services.logistique.reapprovisionnement import ReapprovisionnementService
from commun.repositories.instances import rapports_service
from services.administration.tableau_bord import tableau_bord_service


class TestIntegrationUC2(unittest.TestCase):
    """Tests integration UC2: Consultation stock central + demandes reapprovisionnement"""
    
    def test_workflow_complet_uc2(self):
        produit = gestion_stocks.consulter_stock_central("2")
        self.assertIsNotNone(produit)
        self.assertEqual(produit.nom, "Snapple")
        
        self.assertTrue(produit.is_stock_low())
        
        from commun.repositories.instances import stock_repo
        fresh_service = ReapprovisionnementService(stock_repo)
        demandes = fresh_service.lister_demandes_en_attente()
        self.assertGreaterEqual(len(demandes), 0)
    
    def test_recherche_produits_integration(self):
        produits = gestion_stocks.rechercher_produits("orange")
        self.assertGreater(len(produits), 0)
        
        produit = produits[0]
        self.assertIn("orange", produit.nom.lower())
        self.assertIsNotNone(produit.stock_central)
        self.assertGreaterEqual(produit.stock_central, 0)


class TestIntegrationUC6(unittest.TestCase):
    """Tests integration UC6: Workflow complet reapprovisionnement"""
    
    def setUp(self):
        from commun.repositories.instances import stock_repo
        self.service = ReapprovisionnementService(stock_repo)
        self.service.stock_repo._demandes = []
    
    def test_workflow_complet_reapprovisionnement(self):
        self.service.stock_repo._demande_counter += 1
        demande_id = f"no{self.service.stock_repo._demande_counter}"
        
        from commun.modeles.produit import DemandeReapprovisionnement
        from datetime import datetime
        demande = DemandeReapprovisionnement(
            id=demande_id,
            magasin_id="magasin 2",
            produit_id="1",
            quantite_demandee=25,
            created_at=datetime.now()
        )
        self.service.stock_repo._demandes.append(demande)
        
        demandes = self.service.lister_demandes_en_attente()
        demande_trouvee = any(d.id == demande_id for d in demandes)
        self.assertTrue(demande_trouvee)
        
        success = self.service.approuver_et_traiter(demande_id)
        self.assertTrue(success)
        
        demande = self.service.obtenir_demande(demande_id)
        self.assertEqual(demande.statut, "TRAITE")
    
    def test_rejet_stock_insuffisant(self):
        self.service.stock_repo._demande_counter += 1
        demande_id = f"no{self.service.stock_repo._demande_counter}"
        
        from commun.modeles.produit import DemandeReapprovisionnement
        from datetime import datetime
        demande = DemandeReapprovisionnement(
            id=demande_id,
            magasin_id="magasin 3",
            produit_id="2",
            quantite_demandee=1000,
            created_at=datetime.now()
        )
        self.service.stock_repo._demandes.append(demande)
        
        success = self.service.valider_demande(demande_id, True)
        self.assertFalse(success)
        
        demande = self.service.obtenir_demande(demande_id)
        self.assertEqual(demande.statut, "REJETE")


class TestIntegrationStockAlert(unittest.TestCase):
    """Tests integration alertes stock faible"""
    
    def test_detection_stock_faible(self):
        produits = gestion_stocks.stock_repo.get_all_produits()
        produits_faible = [p for p in produits if p.is_stock_low()]
        self.assertGreater(len(produits_faible), 0)
        
        for produit in produits_faible:
            self.assertTrue(produit.is_stock_low())
            self.assertLessEqual(produit.stock_central, produit.seuil_critique)


class TestIntegrationRapports(unittest.TestCase):
    """Tests integration generation rapports"""
    
    def test_generation_rapport_consolide(self):
        """Test generation rapport consolide avec donnees"""
        
        rapport = rapports_service.generer_rapport_consolide(30)
        
        self.assertIsNotNone(rapport)
        self.assertIsNotNone(rapport.total_general)
        self.assertIsNotNone(rapport.ventes_par_magasin)
        self.assertIsNotNone(rapport.produits_plus_vendus)
        self.assertIsNotNone(rapport.periode)
        
        self.assertGreaterEqual(len(rapport.ventes_par_magasin), 3)
    
    def test_tableau_bord_generation(self):
        """Test du tableau de bord"""
        
        # Generer tableau bord
        dashboard = tableau_bord_service.generer_tableau_bord()
        
        self.assertIsNotNone(dashboard)
        self.assertIsNotNone(dashboard.total_reseau)
        self.assertIsNotNone(dashboard.performances_magasins)
        self.assertIsNotNone(dashboard.alertes_stock)
        self.assertIsNotNone(dashboard.tendances_hebdomadaires)
        
        self.assertGreaterEqual(len(dashboard.performances_magasins), 5)


class TestIntegrationCompleteWorkflow(unittest.TestCase):
    """Tests integration scenarios complets"""
    
    def setUp(self):
        from commun.repositories.instances import stock_repo
        self.service = ReapprovisionnementService(stock_repo)
        self.service.stock_repo._demandes = []
    
    def test_scenario_complet_magasin(self):
        produit = gestion_stocks.consulter_stock_central("5")
        self.assertIsNotNone(produit)
        
        self.assertTrue(produit.is_stock_low())
        
        demandes = self.service.lister_demandes_en_attente()
        initial_count = len(demandes)
    
    def test_scenario_gestion_complete(self):
        rapport = rapports_service.generer_rapport_consolide(7)
        self.assertIsNotNone(rapport)
        
        dashboard = tableau_bord_service.generer_tableau_bord()
        self.assertIsNotNone(dashboard)
        
        alertes = dashboard.alertes_stock
        if len(alertes) > 0:
            produits = gestion_stocks.stock_repo.get_all_produits()
            produits_faible = [p for p in produits if p.is_stock_low()]
            self.assertGreater(len(produits_faible), 0)


if __name__ == "__main__":
    unittest.main()
