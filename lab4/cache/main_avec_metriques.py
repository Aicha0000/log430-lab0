from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends, status, Security, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from typing import Dict, Any
try:
    from pydantic import BaseModel, Field
except ImportError:
    class BaseModel:
        def __init__(self, **data):
            for key, value in data.items():
                setattr(self, key, value)
        
        def dict(self, exclude_unset=False):
            result = {}
            for key, value in self.__dict__.items():
                if not exclude_unset or value is not None:
                    result[key] = value
            return result
    
    def Field(default=None, **kwargs):
        return default
import uvicorn
import os
from datetime import datetime
import time
import logging
import json
from prometheus_client import Counter, Histogram, Gauge, start_http_server, generate_latest, REGISTRY
REGISTRY._collector_to_names.clear()
REGISTRY._names_to_collectors.clear()
from prometheus_client.openmetrics.exposition import CONTENT_TYPE_LATEST
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'prototype'))

from commun.repositories.instances import rapports_service, gestion_stocks, reappro_service, produits_service
from services.administration.tableau_bord import tableau_bord_service
from cache_manager import cache

# setup du logging - pas fancy mais ca marche
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api_logs.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# metriques prometheus
api_requests_total = Counter('api_requests_total', 'Total API requests', ['method', 'endpoint', 'status'])
api_request_duration_seconds = Histogram('api_request_duration_seconds', 'Request duration in seconds', ['endpoint'])
api_active_requests = Gauge('api_active_requests', 'Active requests')
api_stock_consultations = Counter('api_stock_consultations_total', 'Total stock consultations')
api_reports_generated = Counter('api_reports_generated_total', 'Total reports generated')

# middleware pour metriques
class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        api_active_requests.inc()
        
        try:
            response = await call_next(request)
            duration = time.time() - start_time
            
            api_requests_total.labels(
                method=request.method,
                endpoint=request.url.path,
                status=response.status_code
            ).inc()
            
            api_request_duration_seconds.labels(
                endpoint=request.url.path
            ).observe(duration)
            
            # log structure JSON
            log_data = {
                "timestamp": datetime.now().isoformat(),
                "method": request.method,
                "path": request.url.path,
                "status": response.status_code,
                "duration": round(duration, 3),
                "user_agent": request.headers.get("user-agent", "unknown")
            }
            logger.info(json.dumps(log_data))
            
            return response
            
        except Exception as e:
            duration = time.time() - start_time
            api_requests_total.labels(
                method=request.method,
                endpoint=request.url.path,
                status=500
            ).inc()
            
            logger.error(f"Request error: {str(e)}")
            raise
        finally:
            api_active_requests.dec()

app = FastAPI(title="API Multi-magasins avec Cache", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(MetricsMiddleware)

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    if credentials.credentials != "lab3-static-token":
        raise HTTPException(status_code=401, detail="Token invalide")
    return credentials.credentials

@app.get("/health")
async def health_check():
    cache_status = "connected" if cache.is_connected() else "disconnected"
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "cache": cache_status
    }

@app.get("/api/central")
async def get_stock_central(token: str = Depends(verify_token)):
    api_stock_consultations.inc()
    
    cache_key = "stock_central_all"
    
    # essai de recuperer du cache
    cached_result = cache.get(cache_key)
    if cached_result and cache.is_connected():
        return cached_result
    
    # si pas en cache, aller chercher en DB
    try:
        result = gestion_stocks.consulter_stock_central()
        
        # mettre en cache pour 120 secondes
        if cache.is_connected():
            cache.set(cache_key, result, 120)
        
        return result
    except Exception as e:
        logger.error(f"Error getting stock central: {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur lors de la consultation du stock")

@app.get("/api/consolide")
async def get_rapport_consolide(days: int = 30, token: str = Depends(verify_token)):
    api_reports_generated.inc()
    
    cache_key = f"rapport_consolide_{days}"
    
    # essai cache
    cached_result = cache.get(cache_key)
    if cached_result and cache.is_connected():
        return cached_result
    
    try:
        result = rapports_service.generer_rapport_consolide(days)
        
        # cache pour 300 secondes (5 minutes)
        if cache.is_connected():
            cache.set(cache_key, result, 300)
        
        return result
    except Exception as e:
        logger.error(f"Error generating consolidated report: {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur lors de la generation du rapport")

@app.put("/api/produits/{produit_id}")
async def update_produit(produit_id: str, data: dict, token: str = Depends(verify_token)):
    try:
        result = produits_service.modifier_produit(produit_id, data)
        
        # invalidation cache apres update
        if cache.is_connected():
            cache.delete_pattern("stock_central_*")
            cache.delete_pattern(f"produit_{produit_id}")
            cache.delete_pattern("rapport_consolide_*")
        
        return result
    except Exception as e:
        logger.error(f"Error updating product {produit_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur lors de la mise a jour")

@app.get("/metrics")
async def metrics():
    data = generate_latest(REGISTRY)
    return Response(content=data.decode('utf-8'), media_type="text/plain")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)