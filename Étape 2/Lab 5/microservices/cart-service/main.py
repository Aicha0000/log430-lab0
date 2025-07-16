import time
from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette.responses import Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import psycopg2
from psycopg2.extras import RealDictCursor
import os
import logging

# Configuration du logging pour le service panier
logging.basicConfig(level=logging.INFO, format='%(asctime)s - CART - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(title="Service Panier", version="1.0.0")

# Métriques spécifiques au service panier
panier_requests = Counter('panier_requests_total', 'Total panier requests', ['method', 'endpoint'])
panier_duration = Histogram('panier_request_duration_seconds', 'Panier request duration', buckets=[0.1, 0.5, 1.0, 2.0, 5.0])

class CartItem(BaseModel):
    product_id: str
    nom_produit: str
    quantity: int
    prix_unitaire: float

class AddToCartRequest(BaseModel):
    customer_id: int
    product_id: str
    nom_produit: str
    quantity: int
    prix_unitaire: float

# Configuration de la base de données pour le panier
class PanierDatabase:
    def __init__(self):
        self.db_url = os.getenv("DATABASE_URL", "postgresql://cart:cart@cart-db:5432/cart")
        self.init_db()
    
    def get_connection(self):
        return psycopg2.connect(self.db_url, cursor_factory=RealDictCursor)
    
    def init_db(self):
        """Initialise la table panier si elle n'existe pas"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS panier_items (
                id SERIAL PRIMARY KEY,
                customer_id INTEGER NOT NULL,
                product_id VARCHAR(100) NOT NULL,
                nom_produit VARCHAR(255) NOT NULL,
                quantity INTEGER NOT NULL,
                prix_unitaire DECIMAL(10,2) NOT NULL,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()
        logger.info("Base de données panier initialisée")
    
    def add_item(self, customer_id: int, product_id: str, nom_produit: str, quantity: int, prix_unitaire: float):
        conn = self.get_connection()
        cursor = conn.cursor()
        # Vérifie si l'item existe déjà
        cursor.execute(
            "SELECT id, quantity FROM panier_items WHERE customer_id = %s AND product_id = %s",
            (customer_id, product_id)
        )
        existing = cursor.fetchone()
        
        if existing:
            # Met à jour la quantité
            cursor.execute(
                "UPDATE panier_items SET quantity = quantity + %s WHERE id = %s",
                (quantity, existing['id'])
            )
        else:
            # Ajoute un nouvel item
            cursor.execute(
                "INSERT INTO panier_items (customer_id, product_id, nom_produit, quantity, prix_unitaire) VALUES (%s, %s, %s, %s, %s)",
                (customer_id, product_id, nom_produit, quantity, prix_unitaire)
            )
        
        conn.commit()
        cursor.close()
        conn.close()
    
    def get_panier(self, customer_id: int):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM panier_items WHERE customer_id = %s ORDER BY added_at DESC",
            (customer_id,)
        )
        items = cursor.fetchall()
        cursor.close()
        conn.close()
        return [dict(item) for item in items]
    
    def remove_item(self, customer_id: int, product_id: str):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM panier_items WHERE customer_id = %s AND product_id = %s",
            (customer_id, product_id)
        )
        rows_affected = cursor.rowcount
        conn.commit()
        cursor.close()
        conn.close()
        return rows_affected > 0
    
    def clear_panier(self, customer_id: int):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM panier_items WHERE customer_id = %s",
            (customer_id,)
        )
        conn.commit()
        cursor.close()
        conn.close()

panier_db = PanierDatabase()

@app.middleware("http")
async def panier_metrics_middleware(request, call_next):
    debut_temps = time.time()
    panier_requests.labels(method=request.method, endpoint=request.url.path).inc()
    response = await call_next(request)
    duree = time.time() - debut_temps
    panier_duration.observe(duree)
    logger.info(f"Requête {request.method} {request.url.path} - Durée: {duree:.3f}s")
    return response

@app.get("/health")
async def health_check():
    # Vérification de la santé du service panier
    try:
        conn = panier_db.get_connection()
        conn.close()
        return {"status": "healthy", "service": "panier", "database": "connected"}
    except Exception as e:
        logger.error(f"Problème de santé détecté: {e}")
        raise HTTPException(status_code=503, detail="Service panier indisponible")

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.post("/panier/add")
async def ajouter_au_panier(item_data: AddToCartRequest):
    # Validation manuelle pour certains champs
    if item_data.quantity <= 0:
        raise HTTPException(status_code=422, detail="La quantité doit être positive")
    
    if item_data.prix_unitaire < 0:
        raise HTTPException(status_code=422, detail="Le prix ne peut pas être négatif")
    
    try:
        panier_db.add_item(
            item_data.customer_id,
            item_data.product_id,
            item_data.nom_produit,
            item_data.quantity,
            item_data.prix_unitaire
        )
        logger.info(f"Article ajouté au panier du client {item_data.customer_id}")
        return {"message": "Article ajouté au panier avec succès", "product_id": item_data.product_id}
    except Exception as e:
        logger.error(f"Erreur lors de l'ajout au panier: {e}")
        raise HTTPException(status_code=500, detail="Erreur interne du service panier")

@app.get("/panier/{customer_id}")
async def consulter_panier(customer_id: int):
    try:
        items = panier_db.get_panier(customer_id)
        total = sum(item["quantity"] * float(item["prix_unitaire"]) for item in items)
        
        return {
            "client_id": customer_id,
            "articles": items,
            "total_prix": round(total, 2),
            "nombre_articles": len(items)
        }
    except Exception as e:
        logger.error(f"Erreur consultation panier client {customer_id}: {e}")
        raise HTTPException(status_code=500, detail="Impossible de consulter le panier")

@app.delete("/panier/{customer_id}/item/{product_id}")
async def retirer_du_panier(customer_id: int, product_id: str):
    try:
        success = panier_db.remove_item(customer_id, product_id)
        if not success:
            raise HTTPException(status_code=404, detail="Article non trouvé dans le panier")
        
        logger.info(f"Article {product_id} retiré du panier du client {customer_id}")
        return {"message": "Article retiré avec succès", "product_id": product_id}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur suppression article panier: {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la suppression")

@app.delete("/panier/{customer_id}/clear")
async def vider_panier(customer_id: int):
    try:
        panier_db.clear_panier(customer_id)
        logger.info(f"Panier du client {customer_id} vidé")
        return {"message": "Panier vidé avec succès", "client_id": customer_id}
    except Exception as e:
        logger.error(f"Erreur vidage panier client {customer_id}: {e}")
        raise HTTPException(status_code=500, detail="Impossible de vider le panier")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8007)