import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from commun.repositories.postgresql_stock_repository import PostgreSQLStockRepository
from commun.repositories.postgresql_vente_repository import PostgreSQLVenteRepository
from services.logistique.gestion_stocks import GestionStocks
from services.administration.rapports_consolides import RapportsConsolides
from services.logistique.reapprovisionnement import ReapprovisionnementService
from services.administration.gestion_produits import GestionProduitsService

stock_repo = PostgreSQLStockRepository()
vente_repo = PostgreSQLVenteRepository()

gestion_stocks = GestionStocks(stock_repo)
rapports_service = RapportsConsolides(vente_repo)
reappro_service = ReapprovisionnementService(stock_repo)
produits_service = GestionProduitsService(stock_repo)
