# LOG430 - Projet Multi-Magasins

## Structure organisée

### Étape 1 (Labs 0-2)
Contient tous les éléments des premiers labs déjà remis au professeur:
- Documentation d'architecture (ADR, ARC42)
- Diagrammes UML 
- Prototypes et services métier
- Tests unitaires et d'intégration
- Base de données et modèles

### Lab 3 
Contient uniquement les éléments spécifiques au Lab 3:
- Application FastAPI de production
- Tests de validation Lab 3
- Configuration Docker
- Documentation finale

## Lab 3 - Tests automatisés

Pour tester tous les requirements Lab 3:

```bash
cd "Lab 3"
python3 -m venv venv
source venv/bin/activate  
pip install requests
python lab3/test_lab3.py
```

## Démarrage

```bash
cd "Lab 3"
docker-compose up -d
```

Accès: http://localhost:8000/docs