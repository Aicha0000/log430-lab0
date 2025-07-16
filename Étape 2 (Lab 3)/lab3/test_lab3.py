#!/usr/bin/env python3
"""
Tests Lab 3 - Verification complete des requirements
"""
import unittest
import requests
import json

API_BASE = "http://localhost:8000"
TOKEN = "lab3-static-token"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}
INVALID_HEADERS = {"Authorization": "Bearer invalid-token"}

class TestLab3Authentication(unittest.TestCase):
    """Tests authentification Lab 3"""
    
    def test_endpoints_require_auth(self):
        """Test que les endpoints protégés requièrent l'authentification"""
        protected_endpoints = [
            "/api/consolide",
            "/api/central", 
            "/api/dashboard",
            "/api/produits",
            "/api/alertes/faible-stock"
        ]
        
        for endpoint in protected_endpoints:
            with self.subTest(endpoint=endpoint):
                response = requests.get(f"{API_BASE}{endpoint}")
                self.assertIn(response.status_code, [401, 403])
    
    def test_valid_token_access(self):
        """Test que le token valide donne accès"""
        response = requests.get(f"{API_BASE}/api/central", headers=HEADERS)
        self.assertEqual(response.status_code, 200)
    
    def test_invalid_token_denied(self):
        """Test que le token invalide est refusé"""
        response = requests.get(f"{API_BASE}/api/central", headers=INVALID_HEADERS)
        self.assertEqual(response.status_code, 401)

class TestLab3Documentation(unittest.TestCase):
    """Tests documentation Swagger"""
    
    def test_swagger_ui_accessible(self):
        """Test que Swagger UI est accessible"""
        response = requests.get(f"{API_BASE}/docs")
        self.assertEqual(response.status_code, 200)
        self.assertIn("swagger", response.text.lower())
    
    def test_openapi_spec_accessible(self):
        """Test que la spec OpenAPI est accessible"""
        response = requests.get(f"{API_BASE}/openapi.json")
        self.assertEqual(response.status_code, 200)
        
        spec = response.json()
        self.assertEqual(spec["info"]["title"], "Lab 3 - API Multi-Magasins")
        self.assertEqual(spec["info"]["version"], "1.0.0")

class TestLab3RESTBestPractices(unittest.TestCase):
    """Tests bonnes pratiques REST"""
    
    def test_http_verbs_usage(self):
        """Test utilisation correcte des verbes HTTP"""
        # GET pour consultation
        response = requests.get(f"{API_BASE}/api/central", headers=HEADERS)
        self.assertEqual(response.status_code, 200)
        
        # PUT pour mise à jour
        payload = {"name": "Test Product", "price": 29.99, "description": "Test description"}
        response = requests.put(f"{API_BASE}/api/produits/P001", headers=HEADERS, json=payload)
        self.assertIn(response.status_code, [200, 400])  # 200 si existe, 400 si n'existe pas
        
        # POST pour création/action
        sale_payload = {"Id_produit": "P001", "quantite": 1}
        response = requests.post(f"{API_BASE}/api/magasin/1/vente", headers=HEADERS, json=sale_payload)
        self.assertIn(response.status_code, [200, 400, 404])
    
    def test_http_status_codes(self):
        """Test codes de statut HTTP standards"""
        # 200 pour succès
        response = requests.get(f"{API_BASE}/api/central", headers=HEADERS)
        self.assertEqual(response.status_code, 200)
        
        # 401 pour authentification manquante
        response = requests.get(f"{API_BASE}/api/central")
        self.assertIn(response.status_code, [401, 403])
        
        # 404 pour ressource inexistante
        response = requests.get(f"{API_BASE}/api/central/produit/INEXISTANT", headers=HEADERS)
        self.assertEqual(response.status_code, 404)
        
        # 422 pour données invalides
        invalid_payload = {"name": "", "price": -10, "description": "test"}
        response = requests.put(f"{API_BASE}/api/produits/P001", headers=HEADERS, json=invalid_payload)
        self.assertEqual(response.status_code, 422)
    
    def test_error_messages_structure(self):
        """Test structure des messages d'erreur"""
        # Test erreur 404
        response = requests.get(f"{API_BASE}/api/central/produit/INEXISTANT", headers=HEADERS)
        self.assertEqual(response.status_code, 404)
        error_data = response.json()
        self.assertIn("detail", error_data)
        self.assertIn("not found", error_data["detail"].lower())
        
        # Test erreur validation
        invalid_payload = {"name": "", "price": -10}
        response = requests.put(f"{API_BASE}/api/produits/P001", headers=HEADERS, json=invalid_payload)
        self.assertEqual(response.status_code, 422)
        error_data = response.json()
        self.assertIn("detail", error_data)

class TestLab3Deployment(unittest.TestCase):
    """Tests déploiement et exécution"""
    
    def test_api_accessibility(self):
        """Test accessibilité de l'API"""
        response = requests.get(f"{API_BASE}/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
    
    def test_web_interface_available(self):
        """Test interface web disponible"""
        response = requests.get(f"{API_BASE}/web")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Tableau de Bord", response.text)

if __name__ == "__main__":
    print("Tests automatisés Lab 3 - Verification complète")
    print("=" * 50)
    unittest.main(verbosity=2)