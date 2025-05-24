"""
Tests unitaires pour le système de caisse.
"""
from app.models import Produit, Vente, LigneVente
from app.persistance.db import session


def test_produit_creation():
    """Test la création d'un produit."""
    produit = Produit(nom="Test Produit", prix=7.99, description="Test", stock=3)
    assert produit.nom == "Test Produit"
    assert produit.prix == 7.99
    assert produit.stock == 3


def test_vente_creation():
    """Test la création d'une vente."""
    vente = Vente(total=21.50)
    assert vente.total == 21.50
    assert vente.statut == 'active'


def test_ligne_vente_creation():
    """Test la création d'une ligne de vente."""
    ligne = LigneVente(vente_id=1, produit_id=1, quantite=2, prix_unitaire=7.99)
    assert ligne.quantite == 2
    assert ligne.prix_unitaire == 7.99


def test_database_connection():
    """Test la connexion à la base de données."""
    # Test simple de connexion
    produits = session.query(Produit).all()
    assert isinstance(produits, list)
        