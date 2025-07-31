from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum
import requests
import time
import json
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response

app = FastAPI(title="Saga Orchestrateur", version="1.0.0")

class EtatCommande(Enum):
    CREEE = "creee"
    STOCK_VERIFIE = "stock_verifie"
    STOCK_RESERVE = "stock_reserve"
    PAIEMENT_TRAITE = "paiement_traite"
    CONFIRMEE = "confirmee"
    ECHEC = "echec"
    ANNULEE = "annulee"

class CommandeRequest(BaseModel):
    customer_id: int
    product_id: int
    quantite: int
    prix_unitaire: float

# metriques saga
saga_total = Counter('saga_total', 'Total sagas executees', ['resultat'])
saga_duration = Histogram('saga_duration_seconds', 'Duree sagas')
saga_etapes = Counter('saga_etapes_total', 'Etapes saga', ['etape', 'resultat'])

# stockage simple des commandes en cours
commandes_saga = {}

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "saga-orchestrateur"}

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.post("/saga/commande")
async def creer_commande_saga(commande: CommandeRequest):
    commande_id = f"cmd_{int(time.time())}"
    
    print(f"Debut saga commande {commande_id}")
    
    # init etat saga
    saga_state = {
        "commande_id": commande_id,
        "customer_id": commande.customer_id,
        "product_id": commande.product_id,
        "quantite": commande.quantite,
        "prix_unitaire": commande.prix_unitaire,
        "etat": EtatCommande.CREEE.value,
        "etapes_completees": []
    }
    
    commandes_saga[commande_id] = saga_state
    
    start_time = time.time()
    
    try:
        # Etape 1: verification stock
        print(f"Saga {commande_id} - verification stock")
        if not verifier_stock(saga_state):
            return rollback_saga(commande_id, "stock_insuffisant")
        
        # Etape 2: reservation stock  
        print(f"Saga {commande_id} - reservation stock")
        if not reserver_stock(saga_state):
            return rollback_saga(commande_id, "reservation_echec")
            
        # Etape 3: paiement
        print(f"Saga {commande_id} - traitement paiement")
        if not traiter_paiement(saga_state):
            return rollback_saga(commande_id, "paiement_refuse")
            
        # Etape 4: confirmation commande
        print(f"Saga {commande_id} - confirmation")
        if not confirmer_commande(saga_state):
            return rollback_saga(commande_id, "confirmation_echec")
        
        # saga reussie
        saga_state["etat"] = EtatCommande.CONFIRMEE.value
        duration = time.time() - start_time
        saga_duration.observe(duration)
        saga_total.labels(resultat="succes").inc()
        
        print(f"Saga {commande_id} terminee avec succes")
        
        return {
            "commande_id": commande_id,
            "etat": saga_state["etat"],
            "duree": round(duration, 2)
        }
        
    except Exception as e:
        print(f"Erreur saga {commande_id}: {str(e)}")
        return rollback_saga(commande_id, f"erreur_technique: {str(e)}")

def verifier_stock(saga_state):
    saga_etapes.labels(etape="verification_stock", resultat="debut").inc()
    
    try:
        # appel inventory service
        response = requests.get(
            f"http://inventory-service:8002/inventory/{saga_state['product_id']}"
        )
        
        if response.status_code != 200:
            saga_etapes.labels(etape="verification_stock", resultat="echec").inc()
            return False
            
        stock_data = response.json()
        if stock_data.get("quantity", 0) < saga_state["quantite"]:
            print(f"Stock insuffisant: {stock_data.get('quantity', 0)} < {saga_state['quantite']}")
            saga_etapes.labels(etape="verification_stock", resultat="echec").inc()
            return False
        
        saga_state["etat"] = EtatCommande.STOCK_VERIFIE.value
        saga_state["etapes_completees"].append("stock_verifie")
        saga_etapes.labels(etape="verification_stock", resultat="succes").inc()
        return True
        
    except Exception as e:
        print(f"Erreur verification stock: {e}")
        saga_etapes.labels(etape="verification_stock", resultat="echec").inc()
        return False

def reserver_stock(saga_state):
    saga_etapes.labels(etape="reservation_stock", resultat="debut").inc()
    
    try:
        # appel pour reserver
        payload = {
            "product_id": saga_state["product_id"],
            "quantity": saga_state["quantite"],
            "commande_id": saga_state["commande_id"]
        }
        
        response = requests.post(
            "http://inventory-service:8002/inventory/reserve",
            json=payload
        )
        
        if response.status_code != 200:
            saga_etapes.labels(etape="reservation_stock", resultat="echec").inc()
            return False
        
        saga_state["etat"] = EtatCommande.STOCK_RESERVE.value
        saga_state["etapes_completees"].append("stock_reserve")
        saga_etapes.labels(etape="reservation_stock", resultat="succes").inc()
        return True
        
    except Exception as e:
        print(f"Erreur reservation stock: {e}")
        saga_etapes.labels(etape="reservation_stock", resultat="echec").inc()
        return False

def traiter_paiement(saga_state):
    saga_etapes.labels(etape="paiement", resultat="debut").inc()
    
    try:
        montant_total = saga_state["quantite"] * saga_state["prix_unitaire"]
        
        payload = {
            "customer_id": saga_state["customer_id"],
            "montant": montant_total,
            "commande_id": saga_state["commande_id"]
        }
        
        response = requests.post(
            "http://payment-service:8009/payment/process",
            json=payload
        )
        
        if response.status_code != 200:
            saga_etapes.labels(etape="paiement", resultat="echec").inc()
            return False
        
        saga_state["etat"] = EtatCommande.PAIEMENT_TRAITE.value
        saga_state["etapes_completees"].append("paiement_traite")
        saga_etapes.labels(etape="paiement", resultat="succes").inc()
        return True
        
    except Exception as e:
        print(f"Erreur paiement: {e}")
        saga_etapes.labels(etape="paiement", resultat="echec").inc()
        return False

def confirmer_commande(saga_state):
    saga_etapes.labels(etape="confirmation", resultat="debut").inc()
    
    try:
        payload = {
            "customer_id": saga_state["customer_id"],
            "product_id": saga_state["product_id"],
            "quantity": saga_state["quantite"],
            "total_amount": saga_state["quantite"] * saga_state["prix_unitaire"],
            "status": "confirmed"
        }
        
        response = requests.post(
            "http://order-service:8007/orders",
            json=payload
        )
        
        if response.status_code not in [200, 201]:
            saga_etapes.labels(etape="confirmation", resultat="echec").inc()
            return False
        
        saga_state["etapes_completees"].append("commande_confirmee")
        saga_etapes.labels(etape="confirmation", resultat="succes").inc()
        return True
        
    except Exception as e:
        print(f"Erreur confirmation: {e}")
        saga_etapes.labels(etape="confirmation", resultat="echec").inc()
        return False

def rollback_saga(commande_id, raison):
    print(f"Rollback saga {commande_id} - {raison}")
    
    saga_state = commandes_saga.get(commande_id)
    if not saga_state:
        return {"error": "saga non trouvee"}
    
    # compensation selon etapes completees
    etapes_completees = saga_state.get("etapes_completees", [])
    
    # liberer stock si reserve
    if "stock_reserve" in etapes_completees:
        print(f"Liberation stock pour {commande_id}")
        try:
            requests.post(
                "http://inventory-service:8002/inventory/release",
                json={"commande_id": commande_id}
            )
        except Exception as e:
            print(f"Erreur liberation stock: {e}")
    
    # annuler paiement si traite
    if "paiement_traite" in etapes_completees:
        print(f"Annulation paiement pour {commande_id}")
        try:
            requests.post(
                "http://payment-service:8009/payment/cancel",
                json={"commande_id": commande_id}
            )
        except Exception as e:
            print(f"Erreur annulation paiement: {e}")
    
    saga_state["etat"] = EtatCommande.ANNULEE.value
    saga_total.labels(resultat="echec").inc()
    
    return {
        "commande_id": commande_id,
        "etat": "echec",
        "raison": raison,
        "etapes_completees": etapes_completees
    }

@app.get("/saga/commande/{commande_id}")
async def get_saga_status(commande_id: str):
    saga_state = commandes_saga.get(commande_id)
    if not saga_state:
        raise HTTPException(status_code=404, detail="Commande non trouvee")
    
    return saga_state

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8010)