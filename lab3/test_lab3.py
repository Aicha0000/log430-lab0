#!/usr/bin/env python3
"""
Tests Lab 3 - Authentication et Documentation
"""
import unittest
import requests

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

if __name__ == "__main__":
    unittest.main()