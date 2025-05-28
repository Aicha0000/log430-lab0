"""
Tests unitaires pour le système de caisse.
"""
from app.models import Produit, Vente, LigneVente


def test_produit_creation():
    """Test la création d'un produit."""
    produit = Produit(nom="Test", prix=5.99, stock=10)
    assert produit.nom == "Test"
    assert produit.prix == 5.99
    assert produit.stock == 10


def test_vente_creation():
    """Test la création d'une vente."""
    vente = Vente(total=15.99, statut='active')
    assert vente.total == 15.99
    assert vente.statut == 'active'


def test_ligne_vente_creation():
    """Test la création d'une ligne de vente."""
    ligne = LigneVente(vente_id=1, produit_id=1, quantite=3, prix_unitaire=5.99)
    assert ligne.vente_id == 1
    assert ligne.produit_id == 1
    assert ligne.quantite == 3
    assert ligne.prix_unitaire == 5.99


def test_models_import():
    """Test que les modèles peuvent être importés."""
    assert Produit is not None
    assert Vente is not None
    assert LigneVente is not None
        