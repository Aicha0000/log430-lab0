# Service d'inventaire - gestion des stocks
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
from fastapi import FastAPI, HTTPException
import time
from typing import List, Optional
import logging

# Configuration du logging pour l'inventaire
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - INVENTORY - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(title="Inventaire Service", version="1.0.0")

# Compteurs pour l'inventaire
inventory_ops = Counter('inventory_operations_total', 'Total inventory operations', ['method', 'endpoint'])
inventory_time = Histogram('inventory_operation_duration_seconds', 'Inventory operation duration', buckets=[0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0])

class GestionnaireStock:
    def __init__(self):
        # Données de stock temporaires
        self.stock_magasins = {
            "1": {"product_id": "1", "store_id": "1", "quantity": 50, "reserved": 0},
            "2": {"product_id": "2", "store_id": "1", "quantity": 100, "reserved": 5},
            "3": {"product_id": "3", "store_id": "2", "quantity": 25, "reserved": 2}
        }
    
    def consulter_stock(self, product_id: str):
        """Consultation du stock pour un produit"""
        for item in self.stock_magasins.values():
            if item["product_id"] == product_id:
                return item
        return None
    
    def obtenir_tout_stock(self):
        """Récupération de tout le stock"""
        return list(self.stock_magasins.values())
    
    def mettre_a_jour_stock(self, product_id: str, quantity: int):
        """Mise à jour du stock"""
        for key, item in self.stock_magasins.items():
            if item["product_id"] == product_id:
                item["quantity"] = quantity
                return True
        return False

gestionnaire_stock = GestionnaireStock()

@app.middleware("http")
async def inventory_middleware(request, call_next):
    t1 = time.time()
    inventory_ops.labels(method=request.method, endpoint=request.url.path).inc()
    response = await call_next(request)
    inventory_time.observe(time.time() - t1)
    return response

@app.get("/health")
async def health():
    """Vérification santé du service inventaire"""
    return {"status": "healthy", "service": "inventaire"}

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/inventory/central")
async def get_stock_central():
    stock = gestionnaire_stock.obtenir_tout_stock()
    logger.warning(f"Consultation stock central - {len(stock)} articles")
    return {"data": stock, "total_items": len(stock)}

@app.get("/inventory/{product_id}")
async def get_product_stock(product_id: str):
    stock = gestionnaire_stock.consulter_stock(product_id)
    if not stock:
        raise HTTPException(status_code=404, detail="Produit non trouvé en stock")
    logger.warning(f"Consultation stock pour produit {product_id}")
    return {"data": stock, "product_id": product_id}

@app.put("/inventory/{product_id}")
async def update_stock(product_id: str, quantity: int):
    # Validation manuelle
    if quantity < 0:
        raise HTTPException(status_code=422, detail="Quantité ne peut pas être négative")
    
    success = gestionnaire_stock.mettre_a_jour_stock(product_id, quantity)
    if not success:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    logger.warning(f"Stock mis à jour: {product_id} = {quantity}")
    return {"message": "Stock mis à jour avec succès", "product_id": product_id, "new_quantity": quantity}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
