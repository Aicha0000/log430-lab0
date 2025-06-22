from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from typing import Dict, Any
from pydantic import BaseModel
import uvicorn
import os
from datetime import datetime

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'prototype'))

from commun.repositories.instances import rapports_service, gestion_stocks, reappro_service, produits_service
from services.administration.tableau_bord import tableau_bord_service

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
    title="Lab 3 - API Multi-Magasins",
    description="API RESTful pour système multi-magasins avec centre logistique et maison mère", 
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

from fastapi.openapi.docs import get_swagger_ui_html

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return HTMLResponse(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link type="text/css" rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css">
        <title>{app.title} - Documentation</title>
    </head>
    <body>
        <div id="swagger-ui"></div>
        <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
        <script>
        const ui = SwaggerUIBundle({{
            url: '{app.openapi_url}',
            dom_id: '#swagger-ui',
            presets: [
                SwaggerUIBundle.presets.apis,
                SwaggerUIBundle.presets.standalone
            ],
            layout: "StandaloneLayout",
            deepLinking: true,
            showExtensions: true,
            showCommonExtensions: true,
        }});
        </script>
    </body>
    </html>
    """)

# DTOs
class ProduitUpdate(BaseModel):
    name: str = None
    price: float = None
    description: str = None

class VenteRequest(BaseModel):
    Id_produit: str
    quantite: int = 1

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://webhook.site/unique-id-here")

@app.get("/", tags=["System"])
async def root():
    return {"message": "Lab 3 API Multi-Magasins", "status": "ok"}

@app.get("/health", tags=["System"])
async def health_check():
    return {
        "status": "healthy",
        "services": {
            "database": "ok",
            "api": "ok"
        }
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

# PROTECTED ENDPOINTS - Standard approach
@app.get("/api/consolide", tags=["Rapports"], dependencies=[Depends(get_current_user)])
async def get_consolidated_report(days: int = 30):
    """UC1 - Génère un rapport consolidé des ventes"""
    report = rapports_service.generer_rapport_consolide(days)
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
    products = gestion_stocks.list_all()
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
    product = gestion_stocks.get_stock(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    
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
    """UC4 - Mise à jour d'un produit"""
    success = produits_service.modifier_produit(
        product_id,
        update_data.name,
        update_data.price,
        update_data.description
    )
    
    if success:
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
    if magasin_id < 1 or magasin_id > 5:
        raise HTTPException(status_code=400, detail="ID du magasin doit être entre 1 et 5")
    
    product = gestion_stocks.get_stock(str(sale_data.Id_produit))
    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    
    if product.stock_central < sale_data.quantite:
        raise HTTPException(status_code=400, detail="Stock insuffisant")
    
    total_price = float(product.prix) * sale_data.quantite
    
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
            "source": "Lab3-API",
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
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)