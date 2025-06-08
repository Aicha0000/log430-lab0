#!/usr/bin/env python3
"""
Tests Unitaires - Lab 2
Tests des composants individuels (modeles, repositories, services)
"""
import unittest
import sys
import os
import uuid
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'prototype'))

from commun.modeles.produit import Produit, DemandeReapprovisionnement
from commun.repositories.stock_repository import StockRepository
from commun.repositories.postgresql_stock_repository import PostgreSQLStockRepository
from services.logistique.gestion_stocks import GestionStocks
from services.logistique.reapprovisionnement import ReapprovisionnementService


class TestModeles(unittest.TestCase):
    """Tests unitaires des modeles de donnees"""
    
    def test_produit_creation(self):
        produit = Produit(
            id="1",
            nom="Test Produit",
            description="Description test",
            prix=2.99,
            stock_central=50,
            seuil_critique=10
        )
        
        self.assertEqual(produit.id, "1")
        self.assertEqual(produit.nom, "Test Produit")
        self.assertEqual(produit.prix, 2.99)
        self.assertEqual(produit.stock_central, 50)
        self.assertFalse(produit.is_stock_low())
    
    def test_produit_stock_faible(self):
        produit = Produit(
            id="2",
            nom="Produit Stock Faible",
            description="Test",
            prix=1.99,
            stock_central=5,
            seuil_critique=10
        )
        
        self.assertTrue(produit.is_stock_low())
    
    def test_demande_reapprovisionnement_creation(self):
        demande = DemandeReapprovisionnement(
            id="no1",
            magasin_id="magasin 1",
            produit_id="1",
            quantite_demandee=20
        )
        
        self.assertEqual(demande.id, "no1")
        self.assertEqual(demande.magasin_id, "magasin 1")
        self.assertEqual(demande.quantite_demandee, 20)
        self.assertEqual(demande.statut, "EN_ATTENTE")


class TestStockRepository(unittest.TestCase):
    """Tests unitaires du repository de stock"""
    
    def setUp(self):
        self.repo = PostgreSQLStockRepository()
    
    def test_get_produit_by_id(self):
        produit = self.repo.get_produit_by_id("1")
        self.assertIsNotNone(produit)
        self.assertEqual(produit.id, "1")
        self.assertIsNotNone(produit.nom)
    
    def test_get_produit_inexistant(self):
        produit = self.repo.get_produit_by_id("999")
        self.assertIsNone(produit)
    
    def test_get_all_produits(self):
        produits = self.repo.get_all_produits()
        self.assertEqual(len(produits), 5)
    
    def test_search_produits(self):
        produits = self.repo.search_produits("Coca")
        self.assertGreaterEqual(len(produits), 0)
        if len(produits) > 0:
            self.assertIn("1", [p.id for p in produits]) 


class TestGestionStocks(unittest.TestCase):
    """Tests unitaires du service de gestion des stocks"""
    
    def setUp(self):
        self.repo = PostgreSQLStockRepository()
        self.service = GestionStocks(self.repo)
    
    def test_get_stock_existant(self):
        produit = self.service.get_stock("1")
        self.assertIsNotNone(produit)
        self.assertEqual(produit.id, "1")
        self.assertIsNotNone(produit.nom)
    
    def test_get_stock_inexistant(self):
        produit = self.service.get_stock("999")
        self.assertIsNone(produit)
    
    def test_search_produits(self):
        produits = self.service.search("orange")
        self.assertGreater(len(produits), 0)
    
    def test_list_all_produits(self):
        produits = self.service.list_all()
        self.assertEqual(len(produits), 5)


class TestReapprovisionnementService(unittest.TestCase):
    """Tests unitaires du service de reapprovisionnement"""
    
    def setUp(self):
        self.stock_repo = PostgreSQLStockRepository()
        self.service = ReapprovisionnementService(self.stock_repo)
    
    def test_creer_demande_et_valider(self):
        from commun.modeles.produit import DemandeReapprovisionnement
        
        unique_id = f"test_{uuid.uuid4().hex[:8]}"
        
        demande = DemandeReapprovisionnement(
            id=unique_id,
            magasin_id="magasin 1",
            produit_id="1",
            quantite_demandee=15,
            created_at=datetime.now()
        )
        
        success = self.service.stock_repo.create_demande_reapprovisionnement(demande)
        self.assertTrue(success)
        
        demande_recuperee = self.service.obtenir_demande(unique_id)
        self.assertIsNotNone(demande_recuperee)
        self.assertEqual(demande_recuperee.magasin_id, "magasin 1")
        self.assertEqual(demande_recuperee.quantite_demandee, 15)
    
    def test_valider_demande_approuve(self):
        from commun.modeles.produit import DemandeReapprovisionnement
        

        unique_id = f"test_{uuid.uuid4().hex[:8]}"
        
        demande = DemandeReapprovisionnement(
            id=unique_id,
            magasin_id="magasin 1",
            produit_id="1",
            quantite_demandee=10,
            created_at=datetime.now()
        )
        
        self.service.stock_repo.create_demande_reapprovisionnement(demande)
        
        success = self.service.valider_demande(unique_id, True)
        self.assertTrue(success)
        
        demande_updated = self.service.obtenir_demande(unique_id)
        self.assertEqual(demande_updated.statut, "APPROUVE")
    
    def test_valider_demande_rejete(self):
        from commun.modeles.produit import DemandeReapprovisionnement
        
        unique_id = f"test_{uuid.uuid4().hex[:8]}"
        
        demande = DemandeReapprovisionnement(
            id=unique_id,
            magasin_id="magasin 1",
            produit_id="1",
            quantite_demandee=10,
            created_at=datetime.now()
        )
        
        self.service.stock_repo.create_demande_reapprovisionnement(demande)
        
        success = self.service.valider_demande(unique_id, False, "Test rejet")
        self.assertTrue(success)
        
        demande_updated = self.service.obtenir_demande(unique_id)
        self.assertEqual(demande_updated.statut, "REJETE")
    
    def test_traiter_reapprovisionnement(self):
        from commun.modeles.produit import DemandeReapprovisionnement
        
        unique_id = f"test_{uuid.uuid4().hex[:8]}"
        
        demande = DemandeReapprovisionnement(
            id=unique_id,
            magasin_id="magasin 1",
            produit_id="1",
            quantite_demandee=5,
            created_at=datetime.now()
        )
        
        self.service.stock_repo.create_demande_reapprovisionnement(demande)
        self.service.valider_demande(unique_id, True)
        
        success = self.service.traiter_reapprovisionnement(unique_id)
        self.assertTrue(success)
        
        demande_updated = self.service.obtenir_demande(unique_id)
        self.assertEqual(demande_updated.statut, "TRAITE")
    
    def test_approuver_et_traiter(self):
        from commun.modeles.produit import DemandeReapprovisionnement
        
        unique_id = f"test_{uuid.uuid4().hex[:8]}"
        
        demande = DemandeReapprovisionnement(
            id=unique_id,
            magasin_id="magasin 1",
            produit_id="1",
            quantite_demandee=5,
            created_at=datetime.now()
        )
        
        self.service.stock_repo.create_demande_reapprovisionnement(demande)

        success = self.service.approuver_et_traiter(unique_id)
        self.assertTrue(success)
        
        demande_updated = self.service.obtenir_demande(unique_id)
        self.assertEqual(demande_updated.statut, "TRAITE")


if __name__ == "__main__":
    unittest.main()
