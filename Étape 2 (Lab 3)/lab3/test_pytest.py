#!/usr/bin/env python3
"""
Tests Lab 3 - Version pytest pour CI/CD
"""
import pytest
import requests
import time
import os

API_BASE = "http://localhost:8000"
TOKEN = "lab3-static-token"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

@pytest.fixture(scope="session", autouse=True)
def wait_for_api():
    """Attendre que l'API soit disponible"""
    max_retries = 30
    for i in range(max_retries):
        try:
            response = requests.get(f"{API_BASE}/health", timeout=5)
            if response.status_code == 200:
                return
        except requests.exceptions.RequestException:
            pass
        time.sleep(1)
    pytest.fail("API non disponible après 30 secondes")

class TestAuthentication:
    """Tests authentification"""
    
    def test_protected_endpoints_require_auth(self):
        """Endpoints protégés requièrent authentification"""
        protected_endpoints = [
            "/api/consolide",
            "/api/central", 
            "/api/dashboard",
            "/api/produits",
            "/api/alertes/faible-stock"
        ]
        
        for endpoint in protected_endpoints:
            response = requests.get(f"{API_BASE}{endpoint}")
            assert response.status_code in [401, 403], f"Endpoint {endpoint} devrait être protégé"
    
    def test_valid_token_access(self):
        """Token valide donne accès"""
        response = requests.get(f"{API_BASE}/api/central", headers=HEADERS)
        assert response.status_code == 200
    
    def test_invalid_token_denied(self):
        """Token invalide est refusé"""
        invalid_headers = {"Authorization": "Bearer invalid-token"}
        response = requests.get(f"{API_BASE}/api/central", headers=invalid_headers)
        assert response.status_code == 401

class TestDocumentation:
    """Tests documentation API"""
    
    def test_swagger_ui_accessible(self):
        """Swagger UI accessible"""
        response = requests.get(f"{API_BASE}/docs")
        assert response.status_code == 200
        assert "swagger" in response.text.lower()
    
    def test_openapi_spec_accessible(self):
        """Spécification OpenAPI accessible"""
        response = requests.get(f"{API_BASE}/openapi.json")
        assert response.status_code == 200
        
        spec = response.json()
        assert spec["info"]["title"] == "Lab 3 - API Multi-Magasins"
        assert spec["info"]["version"] == "1.0.0"

class TestRESTBestPractices:
    """Tests bonnes pratiques REST"""
    
    def test_http_status_codes(self):
        """Codes de statut HTTP standards"""
        # 200 pour succès
        response = requests.get(f"{API_BASE}/api/central", headers=HEADERS)
        assert response.status_code == 200
        
        # 401 pour authentification manquante
        response = requests.get(f"{API_BASE}/api/central")
        assert response.status_code in [401, 403]
        
        # 404 pour ressource inexistante
        response = requests.get(f"{API_BASE}/api/central/produit/INEXISTANT", headers=HEADERS)
        assert response.status_code == 404
    
    def test_error_messages_structure(self):
        """Structure des messages d'erreur"""
        response = requests.get(f"{API_BASE}/api/central/produit/INEXISTANT", headers=HEADERS)
        assert response.status_code == 404
        error_data = response.json()
        assert "detail" in error_data
        assert "not found" in error_data["detail"].lower()

class TestAPIEndpoints:
    """Tests endpoints API"""
    
    def test_health_endpoint(self):
        """Endpoint de santé"""
        response = requests.get(f"{API_BASE}/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_central_stock_endpoint(self):
        """UC2 - Stock central"""
        response = requests.get(f"{API_BASE}/api/central", headers=HEADERS)
        assert response.status_code == 200
        data = response.json()
        assert "produits" in data
        assert "produits total" in data
    
    def test_consolidated_report_endpoint(self):
        """UC1 - Rapport consolidé"""
        response = requests.get(f"{API_BASE}/api/consolide", headers=HEADERS)
        assert response.status_code == 200
        data = response.json()
        assert "vente total" in data
        assert "periode en jours" in data
    
    def test_web_interface(self):
        """UC8 - Interface web"""
        response = requests.get(f"{API_BASE}/web")
        assert response.status_code == 200
        assert "Tableau de Bord" in response.text