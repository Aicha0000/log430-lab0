# LOG430 - Projet Multi-Magasins

## Structure du projet

### Étape 1 (Labs 0-2)
Éléments des premiers labs déjà remis:
- Documentation d'architecture (ADR, ARC42)
- Diagrammes UML 
- Prototypes et services métier
- Tests unitaires et d'intégration
- Base de données et modèles

### Étape 2 (Labs 3-5)

#### Lab 3 
Application FastAPI de production avec:
- Tests automatisés
- Configuration Docker
- Validation des requirements

#### Lab 4
Observabilité, load balancing et cache:
- Monitoring Prometheus/Grafana
- Load balancer NGINX
- Cache Redis distribué
- Tests de performance

#### Lab 5
Architecture microservices avec API Gateway:
- 8 microservices indépendants
- Kong API Gateway
- Load balancing via gateway
- Observabilité comparative

## Démarrage Lab 5

```bash
cd "Étape 2/Lab 5"
docker-compose up -d
./setup-kong.sh
```

Accès gateway: http://localhost:8000
