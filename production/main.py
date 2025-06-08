
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from typing import Dict, Any
import uvicorn
import os
from datetime import datetime

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'prototype'))

from commun.repositories.instances import rapports_service, gestion_stocks, reappro_service, produits_service
from services.administration.tableau_bord import tableau_bord_service

app = FastAPI(title="Lab 2 API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

 
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://webhook.site/unique-id-here")

@app.get("/")
async def root():
    return {"message": "Lab 2 API", "status": "ok"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "services": {
            "database": "ok",
            "api": "ok"
        }
    }


@app.get("/web", response_class=HTMLResponse)
async def web_dashboard():
    return HTMLResponse(content="""
    <html>
    <head>
        <title>Tableau de Bord</title>
        <style>
            body { font-family: Arial; margin: 20px; }
            div { margin: 15px 0; padding: 10px; border: 1px solid black; }
        </style>
    </head>
    <body>
        <h1>Tableau de Bord</h1>
        
        <div>
            <h3>Rapports</h3>
            <div id="reports">Chargement...</div>
        </div>
        
        <div>
            <h3>Stock</h3>
            <div id="stock">Chargement...</div>
        </div>
        
        <div>
            <h3>Alertes</h3>
            <div id="alerts">Chargement...</div>
        </div>
        
        <script>
            fetch('/api/consolide')
                .then(r => r.json())
                .then(data => document.getElementById('reports').innerHTML = 'Ventes: ' + data["vente total"])
                .catch(() => document.getElementById('reports').innerHTML = 'Erreur');
            
            fetch('/api/central')
                .then(r => r.json())
                .then(data => document.getElementById('stock').innerHTML = 'Produits: ' + data["produits total"])
                .catch(() => document.getElementById('stock').innerHTML = 'Erreur');
            
            fetch('/api/alertes/faible-stock')
                .then(r => r.json())
                .then(data => document.getElementById('alerts').innerHTML = 'Alertes: ' + data["alertes totale"])
                .catch(() => document.getElementById('alerts').innerHTML = 'Erreur');
        </script>
    </body>
    </html>
    """)


@app.get("/api/consolide")
async def get_consolidated_report(days: int = 30):
    report = rapports_service.generer_rapport_consolide(days)
    return {
        "periode en jours": days,
        "vente total": float(report.total_general),
        "vente par magasin": dict(report.ventes_par_magasin),
        "produit en tendance": list(report.produits_plus_vendus),
        "periode": report.periode
    }


@app.get("/api/central")
async def get_central_stock():
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

@app.get("/api/central/produit/{product_id}")
async def get_product_stock(product_id: str):
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


@app.get("/api/dashboard")
async def get_dashboard():
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


@app.get("/api/produits")
async def get_all_products():
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

@app.put("/api/produits/{product_id}")
async def update_product(product_id: str, update_data: Dict[str, Any], background_tasks: BackgroundTasks):
    success = produits_service.modifier_produit(
        product_id,
        update_data.get("name"),
        update_data.get("price"),
        update_data.get("description")
    )
    
    if success:
        background_tasks.add_task(
            send_external_webhook,
            "mise a jours produit",
            {"id_produit": product_id, "changes": update_data, "timestamp": datetime.now().isoformat()}
        )
        return {"message": "Produit mise a jours", "id_produit": product_id}
    else:
        raise HTTPException(status_code=400, detail="Mise à jour échouée")


@app.get("/api/reapprovisionnement")
async def get_pending_requests():
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

@app.post("/api/reapprovisionnement/{request_id}/approuver")
async def approve_replenishment(request_id: str, background_tasks: BackgroundTasks):
    success = reappro_service.approuver_et_traiter(request_id)
    
    if success:
        background_tasks.add_task(
            send_external_webhook,
            "reapprovisionnement fait",
            {"request_id": request_id, "timestamp": datetime.now().isoformat()}
        )
        return {"message": "reapprovisionnement fait", "id demande": request_id}
    else:
        raise HTTPException(status_code=400, detail="Echec de demande")


@app.get("/api/alertes/faible-stock")
async def get_low_stock_alerts():
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
        "alertes totale": len(low_stock_products),
        "total_alerts": len(low_stock_products)
    }


@app.post("/api/magasin/{magasin_id}/vente")
async def process_store_sale(magasin_id: int, sale_data: Dict[str, Any], background_tasks: BackgroundTasks):
    if magasin_id < 1 or magasin_id > 5:
        raise HTTPException(status_code=400, detail="ID du magasin doit être entre 1 et 5")
    
    product_id = sale_data.get("Id produit")
    quantity = sale_data.get("quantite", 1)
    
    if not product_id:
        raise HTTPException(status_code=400, detail="ID du produit requis")
    
    product = gestion_stocks.get_stock(str(product_id))
    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    
    if product.stock_central < quantity:
        raise HTTPException(status_code=400, detail="Stock insuffisant pour le produit")
    
    total_price = float(product.prix) * quantity
    
    background_tasks.add_task(
        send_external_webhook,
        "vente_effectuee",
        {
            "id magasin": magasin_id,
            "id produit": product_id,
            "quantite": quantity,
            "prix total": total_price,
            "timestamp": datetime.now().isoformat()
        }
    )
    
    return {
        "message": "Vente traitée avec succès",
        "id magasin": magasin_id,
        "id produit": product_id,
        "quantite": quantity,
        "prix total": total_price
    }

@app.get("/api/magasin/{magasin_id}/stock-local")
async def get_store_stock(magasin_id: int):
    if magasin_id < 1 or magasin_id > 5:
        raise HTTPException(status_code=400, detail="Id du magasin doit être entre 1 et 5")
    
    products = gestion_stocks.list_all()
    
    return {
        "id magasin": magasin_id,
        "Produits": [
            {
                "id": p.id,
                "nom": p.nom,
                "stock local": max(0, p.stock_central - (magasin_id * 10)),
                "prix": float(p.prix),
                "faible stock": p.is_stock_low()
            }
            for p in products
        ],
        "Produit total": len(products)
    }

@app.get("/api/magasin/{magasin_id}/status")
async def get_store_status(magasin_id: int):
    if magasin_id < 1 or magasin_id > 5:
        raise HTTPException(status_code=400, detail="ID du magasin doit être entre 1 et 5")
    
    return {
        "id magasin": magasin_id,
        "nom": f"magasin {magasin_id}",
        "status": "operational",
        "last_sync": datetime.now().isoformat()
    }


@app.get("/api/logistique/stock-centrale")
async def get_logistics_stock():
    products = gestion_stocks.list_all()
    return {
        "centre_logistique": "Central Logistique",
        "produits": [
            {
                "id": p.id,
                "nom": p.nom,
                "stock_centrale": p.stock_central,
                "prix": float(p.prix),
                "Disponibilite pour la distribution": p.stock_central > p.seuil_critique
            }
            for p in products
        ],
        "produit total": len(products),
        "stock total": sum(p.stock_central for p in products)
    }

@app.get("/api/logistique/reapprovisionnement")
async def get_logistics_replenishment():
    requests = reappro_service.lister_demandes_en_attente()
    return {
        "centre_logistique": "Central logistique",
        "pending_requests": [
            {
                "id": req.id,
                "id magasin": req.magasin_id,
                "id produit": req.produit_id,
                "quantite": req.quantite_demandee,
                "status": req.statut,
                "priorite": "high" if req.quantite_demandee > 50 else "normal"
            }
            for req in requests
        ],
        "total pending": len(requests)
    }

@app.post("/api/logistique/reapprovisionnement/{magasin_id}")
async def create_replenishment_request(magasin_id: int, request_data: Dict[str, Any], background_tasks: BackgroundTasks):
    if magasin_id < 1 or magasin_id > 5:
        raise HTTPException(status_code=400, detail="ID du magasin doit être entre 1 et 5")
    
    produit_id = request_data.get("produit_id")
    quantity = request_data.get("quantite")
    
    if not produit_id or not quantity:
        raise HTTPException(status_code=400, detail="Produit ID et quantité requis")
    
    background_tasks.add_task(
        send_external_webhook,
        "demande_reapprovisionnement",
        {
            "magasin_id": magasin_id,
            "produit_id": produit_id,
            "quantite": quantity,
            "timestamp": datetime.now().isoformat()
        }
    )
    
    return {
        "message": "Demande de réapprovisionnement créée",
        "magasin_id": magasin_id,
        "produit_id": produit_id,
        "quantite": quantity
    }


@app.get("/api/webhook/config")
async def get_webhook_config():
    return {
        "external_webhook_url": WEBHOOK_URL,
        "status": "ok" if WEBHOOK_URL != "https://webhook.site/unique-id-here" else "not configured"
    }

@app.put("/api/webhook/config")
async def update_webhook_config(config_data: Dict[str, str]):
    global WEBHOOK_URL
    new_url = config_data.get("webhook_url", "")
    
    if not new_url.startswith("https://"):
        raise HTTPException(status_code=400, detail="Webhook URL doit etre HTTPS")
    
    WEBHOOK_URL = new_url
    return {"message": "Updated", "webhook_url": WEBHOOK_URL}

async def send_external_webhook(event_type: str, data: Dict[str, Any]):
    import requests
    
    if WEBHOOK_URL == "https://webhook.site/unique-id-here":
        print(f"Webhook pas configuré. Enverrait: {event_type} - {data}")
        return
    
    try:
        payload = {
            "event_type": event_type,
            "data": data,
            "source": "Lab2-API",
            "timestamp": datetime.now().isoformat()
        }
        
        response = requests.post(
            WEBHOOK_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"Webhook externe envoyé: {event_type} -> {response.status_code}")
        
    except Exception as e:
        print(f"Échec d'envoi webhook externe: {e}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
