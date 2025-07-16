import sys
import os
import time
import logging
from typing import List, Optional

sys.path.append('/app/shared')
from database import DatabaseConfig, BaseRepository, setup_tables
from fastapi import FastAPI, HTTPException
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response

# Setup logging pour le service produits
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - PRODUCTS - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(title="Service Produits", version="1.0.0")

# Métriques pour le catalogue produits
product_requests = Counter('product_requests_total', 'Total product requests', ['method', 'endpoint'])
product_latency = Histogram('product_request_latency_seconds', 'Product request latency')

class ProductService:
    def __init__(self):
        self.db_config = DatabaseConfig()
        self.repo = BaseRepository(self.db_config)
        self.init_db()
    
    def init_db(self):
        setup_tables(self.db_config)
        existing = self.repo.execute_query("SELECT COUNT(*) as count FROM products")
        if existing[0]['count'] == 0:
            self.repo.execute_query(
                "INSERT INTO products (name, description, price, category) VALUES (%s, %s, %s, %s)",
                ("Coke", "355ml can", 2.99, "Drinks")
            )
            self.repo.execute_query(
                "INSERT INTO products (name, description, price, category) VALUES (%s, %s, %s, %s)",
                ("Sprite", "355ml can", 2.79, "Drinks")
            )
            self.repo.execute_query(
                "INSERT INTO products (name, description, price, category) VALUES (%s, %s, %s, %s)",
                ("Apple Juice", "250ml bottle", 3.49, "Drinks")
            )
            self.repo.execute_query(
                "INSERT INTO products (name, description, price, category) VALUES (%s, %s, %s, %s)",
                ("Chocolate Milk", "500ml carton", 4.25, "Drinks")
            )
            self.repo.execute_query(
                "INSERT INTO products (name, description, price, category) VALUES (%s, %s, %s, %s)",
                ("Cafe", "355ml cup", 5.99, "Drinks")
            )
    
    def get_all_products(self):
        return self.repo.execute_query("SELECT * FROM products ORDER BY id")
    
    def get_product_by_id(self, product_id: str):
        result = self.repo.execute_one("SELECT * FROM products WHERE id = %s", (product_id,))
        return result
    
    def update_product(self, product_id: str, data: dict):
        if 'name' in data:
            self.repo.execute_query(
                "UPDATE products SET name = %s WHERE id = %s",
                (data['name'], product_id)
            )
        if 'price' in data:
            self.repo.execute_query(
                "UPDATE products SET price = %s WHERE id = %s",
                (data['price'], product_id)
            )
        return True

product_service = ProductService()

@app.middleware("http")
async def product_metrics_middleware(request, call_next):
    start = time.time()
    product_requests.labels(method=request.method, endpoint=request.url.path).inc()
    response = await call_next(request)
    product_latency.observe(time.time() - start)
    return response

@app.get("/health")
async def health():
    # Simple health check pour les produits
    return {"status": "healthy", "service": "produits"}

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/products")
async def get_products():
    try:
        produits = product_service.get_all_products()
        logger.debug(f"Récupération de {len(produits)} produits")
        return {"data": produits, "count": len(produits)}
    except Exception as e:
        logger.error(f"Erreur récupération produits: {e}")
        raise HTTPException(status_code=500, detail="Erreur catalogue produits")

@app.get("/products/{product_id}")
async def get_product(product_id: str):
    # Validation manuelle de l'ID
    if not product_id or product_id.strip() == "":
        raise HTTPException(status_code=400, detail="ID produit requis")
    
    produit = product_service.get_product_by_id(product_id)
    if not produit:
        raise HTTPException(status_code=404, detail="Produit introuvable")
    return {"data": produit}

@app.put("/products/{product_id}")
async def update_product(product_id: str, data: dict):
    # Validation des données d'entrée
    if 'price' in data and data['price'] < 0:
        raise HTTPException(status_code=422, detail="Prix doit être positif")
    
    success = product_service.update_product(product_id, data)
    if not success:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    logger.info(f"Produit {product_id} mis à jour")
    return {"message": "Produit mis à jour avec succès", "product_id": product_id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
