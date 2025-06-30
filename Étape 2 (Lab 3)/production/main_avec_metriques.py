from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends, status, Security, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from typing import Dict, Any
try:
    from pydantic import BaseModel, Field
except ImportError:
    # fallback si pydantic pas disponible
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
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'Étape 2 (Lab 3)', 'prototype'))

from commun.repositories.instances import rapports_service, gestion_stocks, reappro_service, produits_service
from services.administration.tableau_bord import tableau_bord_service

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

# classe pour les logs structurés - jsp si c'est overkill mais bon
class LoggerThing:
    def __init__(self, logger):
        self.logger = logger
    
    def log_requete(self, method: str, path: str, status_code: int, duration: float, user_id: str = None):
        log_stuff = {
            "timestamp": datetime.now().isoformat(),
            "method": method,
            "path": path,
            "status_code": status_code,
            "response_time_ms": round(duration * 1000, 2),
            "user_id": user_id or "anonymous",
            "type": "api_request"
        }
        self.logger.info(json.dumps(log_stuff))
    
    def log_business_stuff(self, event_type: str, data: Dict[str, Any]):
        log_stuff = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "data": data
        }
        self.logger.info(json.dumps(log_stuff))

mon_logger = LoggerThing(logger)

# metriques prometheus - ca va tracker les trucs importants
REQUEST_COUNT = Counter('api_requests_total', 'Total API requests', ['method', 'endpoint', 'status'])
REQUEST_TIME = Histogram('api_request_duration_seconds', 'Request duration', ['method', 'endpoint'])
ACTIVE_REQUESTS = Gauge('api_active_requests', 'Active requests')

# metriques business pour le prof
metrics_business = {
    'consultations_stock': Counter('stock_consultations_total', 'Total stock consultations'),
    'rapports_generes': Counter('reports_generated_total', 'Total reports generated'),
    'produits_modifies': Counter('products_updated_total', 'Total product updates'),
    'ventes_traitees': Counter('sales_processed_total', 'Total sales processed'),
    'alertes_stock_faible': Gauge('low_stock_alerts_count', 'Current low stock alerts')
}

# middleware pour prometheus - ca capture tout
class MonitoringMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path == "/metrics":
            return await call_next(request)
        
        start_time = time.time()
        ACTIVE_REQUESTS.inc()
        
        try:
            response = await call_next(request)
            duration = time.time() - start_time
            
            # clean endpoint name 
            endpoint = request.url.path
            if endpoint.startswith('/api/'):
                endpoint = endpoint.split('?')[0]
            
            REQUEST_COUNT.labels(
                method=request.method,
                endpoint=endpoint,
                status=response.status_code
            ).inc()
            
            REQUEST_TIME.labels(
                method=request.method,
                endpoint=endpoint
            ).observe(duration)
            
            # log la requete
            mon_logger.log_requete(
                request.method,
                endpoint,
                response.status_code,
                duration,
                getattr(request.state, 'user_id', None)
            )
            
            return response
            
        except Exception as e:
            duration = time.time() - start_time
            REQUEST_COUNT.labels(
                method=request.method,
                endpoint=request.url.path,
                status=500
            ).inc()
            
            mon_logger.log_requete(
                request.method,
                request.url.path,
                500,
                duration
            )
            raise
        finally:
            ACTIVE_REQUESTS.dec()

security = HTTPBearer()
STATIC_TOKEN = "lab3-static-token"

async def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    if credentials.credentials != STATIC_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials

app = FastAPI(
    title="Lab 4 - API Multi-Magasins (avec monitoring)",
    description="API avec metriques prometheus et logs", 
    version="1.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {"name": "System", "description": "Endpoints système"},
        {"name": "Monitoring", "description": "Métriques et monitoring"},
        {"name": "Interface", "description": "Interface web"},
        {"name": "Rapports", "description": "UC1 - Rapports des ventes"},
        {"name": "Stock Central", "description": "UC2 - Stock central"},
        {"name": "Tableau de Bord", "description": "UC3 - Dashboard"},
        {"name": "Gestion Produits", "description": "UC4 - Gestion produits"},
        {"name": "Logistique", "description": "UC6 - Réapprovisionnement"},
        {"name": "Alertes", "description": "UC7 - Alertes stock"},
        {"name": "Magasins", "description": "Opérations magasins"}
    ]
)

# ajouter le middleware
app.add_middleware(MonitoringMiddleware)

# DTOs - meme chose qu'avant
class ProduitUpdate(BaseModel):
    name: str = Field(None, min_length=1, max_length=100)
    price: float = Field(None, gt=0)
    description: str = Field(None, max_length=500)

class VenteRequest(BaseModel):
    Id_produit: str
    quantite: int = 1

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://webhook.site/unique-id-here")

@app.get("/metrics", tags=["Monitoring"])
async def get_metrics():
    """endpoint pour prometheus"""
    from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
    return Response(
        content=generate_latest().decode('utf-8'),
        media_type="text/plain; charset=utf-8"
    )

@app.get("/", tags=["System"])
async def root():
    return {"message": "Lab 4 API Multi-Magasins avec monitoring", "status": "ok", "version": "1.1.0"}

@app.get("/health", tags=["System"])
async def health_check():
    return {
        "status": "healthy",
        "services": {
            "database": "ok",
            "api": "ok",
            "monitoring": "ok"
        },
        "timestamp": datetime.now().isoformat()
    }

@app.get("/web", response_class=HTMLResponse, tags=["Interface"])
async def web_dashboard():
    return HTMLResponse(content="""
    <html>
    <head><title>Tableau de Bord</title></head>
    <body>
        <h1>Tableau de Bord Multi-Magasins</h1>
        <div>
            <h3>Rapports</h3>
            <div id="reports">Loading...</div>
        </div>
        <div>
            <h3>Stock</h3>
            <div id="stock">Loading...</div>
        </div>
        <div>
            <h3>Alertes</h3>
            <div id="alerts">Loading...</div>
        </div>
        <script>
            const headers = {"Authorization": "Bearer lab3-static-token"};
            fetch('/api/consolide', {headers})
                .then(r => r.json())
                .then(data => document.getElementById('reports').innerHTML = 'Ventes: ' + data["vente total"])
                .catch(() => document.getElementById('reports').innerHTML = 'Error');
            
            fetch('/api/central', {headers})
                .then(r => r.json())
                .then(data => document.getElementById('stock').innerHTML = 'Produits: ' + data["produits total"])
                .catch(() => document.getElementById('stock').innerHTML = 'Error');
            
            fetch('/api/alertes/faible-stock', {headers})
                .then(r => r.json())
                .then(data => document.getElementById('alerts').innerHTML = 'Alertes: ' + data["alertes totale"])
                .catch(() => document.getElementById('alerts').innerHTML = 'Error');
        </script>
    </body>
    </html>
    """)

@app.get("/api/consolide", tags=["Rapports"], dependencies=[Depends(get_current_user)])
async def get_consolidated_report(days: int = 30):
    """UC1 - Génère un rapport consolidé des ventes"""
    metrics_business['rapports_generes'].inc()
    
    report = rapports_service.generer_rapport_consolide(days)
    
    mon_logger.log_business_stuff("rapport_genere", {
        "periode_jours": days,
        "total_ventes": float(report.total_general),
        "nb_magasins": len(report.ventes_par_magasin)
    })
    
    return {
        "periode en jours": days,
        "vente total": float(report.total_general),
        "vente par magasin": dict(report.ventes_par_magasin),
        "produit en tendance": list(report.produits_plus_vendus),
        "periode": report.periode
    }

@app.get("/api/central", tags=["Stock Central"], dependencies=[Depends(get_current_user)])
async def get_central_stock():
    """UC2 - Consultation du stock central"""
    metrics_business['consultations_stock'].inc()
    
    products = gestion_stocks.list_all()
    
    mon_logger.log_business_stuff("stock_consulte", {
        "nb_produits": len(products),
        "produits_stock_faible": len([p for p in products if p.is_stock_low()])
    })
    
    return {
        "produits": [
            {
                "id": p.id,
                "nom": p.nom,
                "stock": p.stock_central,
                "prix": float(p.prix),
                "stock faible": p.is_stock_low()
            }
            for p in products
        ],
        "produits total": len(products)
    }

@app.get("/api/central/produit/{product_id}", tags=["Stock Central"], dependencies=[Depends(get_current_user)])
async def get_product_stock(product_id: str):
    """Détails d'un produit spécifique"""
    metrics_business['consultations_stock'].inc()
    
    product = gestion_stocks.get_stock(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return {
        "id": product.id,
        "nom": product.nom,
        "stock": product.stock_central,
        "prix": float(product.prix),
        "description": product.description,
        "stock faible": product.is_stock_low()
    }

@app.get("/api/dashboard", tags=["Tableau de Bord"], dependencies=[Depends(get_current_user)])
async def get_dashboard():
    """UC3 - Tableau de bord des performances"""
    dashboard = tableau_bord_service.generer_tableau_bord()
    
    mon_logger.log_business_stuff("dashboard_consulte", {
        "total_reseau": float(dashboard.total_reseau),
        "nb_magasins": len(dashboard.performances_magasins),
        "nb_alertes": len(dashboard.alertes_stock)
    })
    
    return {
        "date du rapport": dashboard.date_generation.isoformat(),
        "total_network": float(dashboard.total_reseau),
        "Performance magasin": [
            {
                "magasin": perf.magasin_id,
                "vente": float(perf.ventes_totales),
                "performance": perf.performance_relative,
                "transactions": perf.nb_transactions
            }
            for perf in dashboard.performances_magasins
        ],
        "alerte de stock": len(dashboard.alertes_stock),
        "tendance hebdomadaires": [
            {
                "semaine": trend.semaine,
                "vente": float(trend.ventes_totales),
                "evolution": float(trend.evolution),
                "tendance": trend.tendance
            }
            for trend in dashboard.tendances_hebdomadaires
        ]
    }

@app.get("/api/produits", tags=["Gestion Produits"], dependencies=[Depends(get_current_user)])
async def get_all_products():
    """Liste tous les produits"""
    products = produits_service.lister_produits()
    return {
        "produits": [
            {
                "id": p.id,
                "nom": p.nom,
                "prix": float(p.prix),
                "description": p.description,
                "stock": p.stock_central
            }
            for p in products
        ]
    }

@app.put("/api/produits/{product_id}", tags=["Gestion Produits"], dependencies=[Depends(get_current_user)])
async def update_product(product_id: str, update_data: ProduitUpdate, background_tasks: BackgroundTasks):
    """UC4 - Mise à jour d'un produit avec validation inputs"""
    metrics_business['produits_modifies'].inc()
    
    success = produits_service.modifier_produit(
        product_id,
        update_data.name,
        update_data.price,
        update_data.description
    )
    
    if success:
        mon_logger.log_business_stuff("produit_modifie", {
            "product_id": product_id,
            "changes": update_data.dict(exclude_unset=True)
        })
        
        background_tasks.add_task(
            send_external_webhook,
            "mise a jours produit",
            {"id_produit": product_id, "changes": update_data.dict(exclude_unset=True), "timestamp": datetime.now().isoformat()}
        )
        return {"message": "Produit mis à jour", "id_produit": product_id}
    else:
        raise HTTPException(status_code=400, detail="Mise à jour échouée")

@app.get("/api/alertes/faible-stock", tags=["Alertes"], dependencies=[Depends(get_current_user)])
async def get_low_stock_alerts():
    """UC7 - Alertes de stock faible"""
    products = gestion_stocks.stock_repo.get_all_produits()
    low_stock_products = [p for p in products if p.is_stock_low()]
    
    # update la metrique
    metrics_business['alertes_stock_faible'].set(len(low_stock_products))
    
    mon_logger.log_business_stuff("alertes_stock_consultees", {
        "nb_alertes": len(low_stock_products),
        "produits_critiques": [p.id for p in low_stock_products]
    })
    
    if low_stock_products:
        import asyncio
        asyncio.create_task(
            send_external_webhook(
                "faible_stock_detecte",
                {
                    "total_alerts": len(low_stock_products),
                    "produits": [{"id": p.id, "nom": p.nom, "stock": p.stock_central} for p in low_stock_products],
                    "timestamp": datetime.now().isoformat()
                }
            )
        )
    
    return {
        "low_stock_products": [
            {
                "id": p.id,
                "nom": p.nom,
                "stock present": p.stock_central,
                "seuil": p.seuil_critique,
                "severité": "stock faible" if p.stock_central <= p.seuil_critique else "stock normal"
            }
            for p in low_stock_products
        ],
        "alertes totale": len(low_stock_products)
    }

@app.post("/api/magasin/{magasin_id}/vente", tags=["Magasins"], dependencies=[Depends(get_current_user)])
async def process_store_sale(magasin_id: int, sale_data: VenteRequest, background_tasks: BackgroundTasks):
    """Traitement d'une vente en magasin"""
    metrics_business['ventes_traitees'].inc()
    
    if magasin_id < 1 or magasin_id > 5:
        raise HTTPException(status_code=400, detail="ID du magasin doit être entre 1 et 5")
    
    product = gestion_stocks.get_stock(str(sale_data.Id_produit))
    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    
    if product.stock_central < sale_data.quantite:
        raise HTTPException(status_code=400, detail="Stock insuffisant")
    
    total_price = float(product.prix) * sale_data.quantite
    
    mon_logger.log_business_stuff("vente_traitee", {
        "magasin_id": magasin_id,
        "produit_id": sale_data.Id_produit,
        "quantite": sale_data.quantite,
        "prix_total": total_price
    })
    
    background_tasks.add_task(
        send_external_webhook,
        "vente_effectuee",
        {
            "id magasin": magasin_id,
            "id produit": sale_data.Id_produit,
            "quantite": sale_data.quantite,
            "prix total": total_price,
            "timestamp": datetime.now().isoformat()
        }
    )
    
    return {
        "message": "Vente traitée",
        "id magasin": magasin_id,
        "id produit": sale_data.Id_produit,
        "quantite": sale_data.quantite,
        "prix total": total_price
    }

@app.get("/api/reapprovisionnement", tags=["Logistique"], dependencies=[Depends(get_current_user)])
async def get_pending_requests():
    """UC6 - Liste des demandes de réapprovisionnement"""
    requests = reappro_service.lister_demandes_en_attente()
    return {
        "pending_requests": [
            {
                "id": req.id,
                "id magasin": req.magasin_id,
                "id produit": req.produit_id,
                "quantite": req.quantite_demandee,
                "status": req.statut
            }
            for req in requests
        ],
        "total_pending": len(requests)
    }

@app.post("/api/reapprovisionnement/{request_id}/approuver", tags=["Logistique"], dependencies=[Depends(get_current_user)])
async def approve_replenishment(request_id: str, background_tasks: BackgroundTasks):
    """UC6 - Approbation d'une demande de réapprovisionnement"""
    success = reappro_service.approuver_et_traiter(request_id)
    
    if success:
        mon_logger.log_business_stuff("reapprovisionnement_approuve", {
            "request_id": request_id
        })
        
        background_tasks.add_task(
            send_external_webhook,
            "reapprovisionnement fait",
            {"request_id": request_id, "timestamp": datetime.now().isoformat()}
        )
        return {"message": "Réapprovisionnement approuvé", "id demande": request_id}
    else:
        raise HTTPException(status_code=400, detail="Request failed")

async def send_external_webhook(event_type: str, data: Dict[str, Any]):
    import requests
    
    if WEBHOOK_URL == "https://webhook.site/unique-id-here":
        return
    
    try:
        payload = {
            "event_type": event_type,
            "data": data,
            "source": "Lab4-API",
            "timestamp": datetime.now().isoformat()
        }
        
        response = requests.post(
            WEBHOOK_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        
    except Exception as e:
        pass

if __name__ == "__main__":
    # lancer l'api sur le port 8000
    uvicorn.run("main_avec_metriques:app", host="0.0.0.0", port=8000, reload=True)