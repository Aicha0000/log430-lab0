#!/usr/bin/env python3
"""
Tests End-to-End - Lab 2
Tests du systeme complet via API REST
"""
import unittest
import requests
import time
import json

API_BASE = "http://localhost:8000"

def tearDownModule():
    """Reset product names after all E2E tests complete"""
    try:
        reset_data = {
            "name": "Coca-Cola",
            "price": 1.99,
            "description": "Boisson gazeuse classique"
        }
        requests.put(f"{API_BASE}/api/produits/1", json=reset_data, timeout=5)
        print("Product data reset after E2E tests")
    except Exception as e:
        print(f"Warning: Could not reset product data: {e}")

class TestEndToEndAPI(unittest.TestCase):
    """Tests end-to-end via API REST"""
    
    @classmethod
    def setUpClass(cls):
        """Attendre que l'API soit disponible"""
        max_retries = 10
        for i in range(max_retries):
            try:
                response = requests.get(f"{API_BASE}/health", timeout=5)
                if response.status_code == 200:
                    print(f"API disponible apres {i+1} tentatives")
                    return
            except:
                pass
            time.sleep(2)
        
        raise Exception("API non disponible apres 10 tentatives")
    
    def test_api_health(self):
        """Test API health check"""
        response = requests.get(f"{API_BASE}/health")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertIn("services", data)
    
    def test_uc1_rapports_consolides(self):
        response = requests.get(f"{API_BASE}/api/consolide?days=30")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn("vente total", data)
        self.assertIn("vente par magasin", data)
        self.assertIn("produit en tendance", data)
        self.assertIn("periode en jours", data)
        
        self.assertGreaterEqual(data["vente total"], 0)
        self.assertGreaterEqual(len(data["vente par magasin"]), 3)
    
    def test_uc2_stock_central(self):
        response = requests.get(f"{API_BASE}/api/central")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn("produits", data)
        self.assertIn("produits total", data)
        self.assertEqual(data["produits total"], 5)
        
        produit = data["produits"][0]
        self.assertIn("id", produit)
        self.assertIn("nom", produit)
        self.assertIn("stock", produit)
        self.assertIn("prix", produit)
        self.assertIn("stock faible", produit)
        
        response = requests.get(f"{API_BASE}/api/central/produit/1")
        self.assertEqual(response.status_code, 200)
        
        produit_data = response.json()
        self.assertEqual(produit_data["id"], "1")
        self.assertIsNotNone(produit_data["nom"])
    
    def test_uc3_tableau_bord(self):
        response = requests.get(f"{API_BASE}/api/dashboard")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn("total_network", data)
        self.assertIn("Performance magasin", data)
        self.assertIn("alerte de stock", data)
        self.assertIn("tendance hebdomadaires", data)
    
    def test_uc4_gestion_produits(self):
        response = requests.get(f"{API_BASE}/api/produits")
        self.assertEqual(response.status_code, 200)
        
        update_data = {
            "name": "Coca-Cola Test E2E",
            "price": 2.49,
            "description": "Test end-to-end"
        }
        
        response = requests.put(f"{API_BASE}/api/produits/1", json=update_data)
        self.assertEqual(response.status_code, 200)
        
        result = response.json()
        self.assertIn("message", result)
        self.assertEqual(result["id_produit"], "1")
    
    def test_uc6_reapprovisionnement(self):
        response = requests.get(f"{API_BASE}/api/reapprovisionnement")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn("pending_requests", data)
        self.assertIn("total_pending", data)
    
    def test_uc7_alertes_stock(self):
        response = requests.get(f"{API_BASE}/api/alertes/faible-stock")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn("low_stock_products", data)
        self.assertIn("alertes totale", data)
        
        if data["alertes totale"] > 0:
            alerte = data["low_stock_products"][0]
            self.assertIn("id", alerte)
            self.assertIn("nom", alerte)
            self.assertIn("stock present", alerte)
            self.assertIn("seuil", alerte)
            self.assertIn("severité", alerte)
    
    def test_uc8_interface_web(self):
        response = requests.get(f"{API_BASE}/web")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Tableau de Bord", response.text)
        self.assertIn("Rapports", response.text)
        self.assertIn("Stock", response.text)
        self.assertIn("Alertes", response.text)


class TestEndToEndMagasins(unittest.TestCase):
    """Tests end-to-end endpoints magasins"""
    
    def test_endpoints_magasin_1(self):
        response = requests.get(f"{API_BASE}/api/magasin/1/status")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(data["id magasin"], 1)
        self.assertEqual(data["nom"], "magasin 1")
        self.assertEqual(data["status"], "operational")
        
        response = requests.get(f"{API_BASE}/api/magasin/1/stock-local")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(data["id magasin"], 1)
        self.assertIn("Produits", data)
        self.assertGreater(len(data["Produits"]), 0)
    
    def test_vente_magasin(self):
        sale_data = {
            "Id produit": "1",
            "quantite": 2
        }
        
        response = requests.post(f"{API_BASE}/api/magasin/1/vente", json=sale_data)
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn("message", data)
        self.assertEqual(data["id magasin"], 1)
        self.assertEqual(data["id produit"], "1")
        self.assertEqual(data["quantite"], 2)
        self.assertIn("prix total", data)
    
    def test_tous_magasins_operationnels(self):
        for magasin_id in range(1, 6):
            with self.subTest(magasin_id=magasin_id):
                response = requests.get(f"{API_BASE}/api/magasin/{magasin_id}/status")
                self.assertEqual(response.status_code, 200)
                
                data = response.json()
                self.assertEqual(data["id magasin"], magasin_id)
                self.assertEqual(data["nom"], f"magasin {magasin_id}")
                self.assertEqual(data["status"], "operational")


class TestEndToEndLogistique(unittest.TestCase):
    """Tests end-to-end endpoints centre logistique"""
    
    def test_stock_centrale(self):
        response = requests.get(f"{API_BASE}/api/logistique/stock-centrale")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn("centre_logistique", data)
        self.assertIn("produits", data)
        self.assertIn("produit total", data)
        self.assertIn("stock total", data)
        
        self.assertEqual(data["produit total"], 5)
        self.assertGreater(data["stock total"], 0)
    
    def test_reapprovisionnement_logistique(self):
        response = requests.get(f"{API_BASE}/api/logistique/reapprovisionnement")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn("centre_logistique", data)
        self.assertIn("pending_requests", data)
        self.assertIn("total pending", data)
    
    def test_creation_demande_reapprovisionnement(self):
        request_data = {
            "produit_id": "2",
            "quantite": 25
        }
        
        response = requests.post(f"{API_BASE}/api/logistique/reapprovisionnement/1", json=request_data)
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn("message", data)
        self.assertEqual(data["magasin_id"], 1)
        self.assertEqual(data["produit_id"], "2")
        self.assertEqual(data["quantite"], 25)


class TestEndToEndWebhooks(unittest.TestCase):
    """Tests end-to-end configuration webhooks"""
    
    def test_webhook_config(self):
        """Test configuration webhook"""
        response = requests.get(f"{API_BASE}/api/webhook/config")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn("external_webhook_url", data)
        self.assertIn("status", data)
    
    def test_update_webhook_config(self):
        """Test mise a jour configuration webhook"""
        config_data = {
            "webhook_url": "https://httpbin.org/post"
        }
        
        response = requests.put(f"{API_BASE}/api/webhook/config", json=config_data)
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn("message", data)
        self.assertEqual(data["webhook_url"], "https://httpbin.org/post")


class TestEndToEndWorkflowComplet(unittest.TestCase):
    """Tests end-to-end scenarios complets"""
    
    def test_workflow_complet_gestionnaire(self):
        """Test workflow complet gestionnaire: rapports -> alertes -> actions"""
        
        # 1. Consulter rapports
        response = requests.get(f"{API_BASE}/api/consolide?days=7")
        self.assertEqual(response.status_code, 200)
        rapports = response.json()
        
        # 2. Consulter tableau bord
        response = requests.get(f"{API_BASE}/api/dashboard")
        self.assertEqual(response.status_code, 200)
        dashboard = response.json()
        
        # 3. Verifier alertes stock
        response = requests.get(f"{API_BASE}/api/alertes/faible-stock")
        self.assertEqual(response.status_code, 200)
        alertes = response.json()
        
        # 4. Si alertes, modifier prix produit
        if alertes["total_alerts"] > 0:
            produit_alerte = alertes["low_stock_products"][0]
            update_data = {
                "price": 3.99,
                "description": "Prix ajuste suite alerte stock"
            }
            
            response = requests.put(f"{API_BASE}/api/produits/{produit_alerte['id']}", json=update_data)
            self.assertEqual(response.status_code, 200)
    
    def test_workflow_magasin_vers_logistique(self):
        for _ in range(3):
            sale_data = {"Id produit": "2", "quantite": 1}
            response = requests.post(f"{API_BASE}/api/magasin/2/vente", json=sale_data)
            self.assertEqual(response.status_code, 200)
        
        response = requests.get(f"{API_BASE}/api/alertes/faible-stock")
        self.assertEqual(response.status_code, 200)
        alertes = response.json()
        
        produit_2_alerte = any(p["id"] == "2" for p in alertes["low_stock_products"])
        if produit_2_alerte:
            request_data = {"produit_id": "2", "quantite": 50}
            response = requests.post(f"{API_BASE}/api/logistique/reapprovisionnement/2", json=request_data)
            self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
