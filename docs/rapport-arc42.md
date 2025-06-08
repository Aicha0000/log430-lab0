# Rapport d'Architecture Arc42 - Lab 2 Multi-Store Management

## 1. Introduction et Objectifs

### 1.1 Exigences Essentielles
Le système gère cinq magasins, un centre logistique et une maison mère pour les fonctions administratives. Cette évolution depuis le Laboratoire 1 représente un passage d'une architecture 2-tiers vers une solution multi-magasins scalable.

Pour ce laboratoire, les exigences sont classées selon MoSCoW. Les fonctionnalités Must Have incluent la génération de rapports consolidés (UC1), la consultation du stock central (UC2) et le tableau de bord des performances (UC3). Les fonctionnalités Should Have couvrent la gestion des produits (UC4) et le réapprovisionnement (UC6). Finalement, les Could Have comprennent les alertes automatiques (UC7) et l'interface web (UC8).

### 1.2 Objectifs de Qualité
L'architecture doit être évolutive pour supporter de futures interfaces web ou mobiles. La maintenabilité est assurée par une séparation claire des responsabilités via le Patron Repository. La testabilité est facilitée par l'injection de dépendances, permettant de mocker facilement les composants. La cohérence des données entre magasins et maison mère doit être maintenue en tout temps.

### 1.3 Parties Prenantes
- Les employés de magasin utilisent le système pour consulter les stocks et faire des demandes de réapprovisionnement.
- Les gestionnaires de la maison mère génèrent des rapports, consultent le tableau de bord et gèrent les produits.
- Les responsables logistiques valident et traitent les demandes de réapprovisionnement.

## 2. Contraintes

### 2.1 Contraintes Techniques
L'utilisation de PostgreSQL et la conteneurisation avec Docker et Docker Compose est requise pour le déploiement. Python 3.11 minimum doit être utilisé. L'implémentation du Patron Repository avec injection de dépendances est requise.

### 2.2 Contraintes Organisationnelles
Dans le cadre du cours LOG430, le développement se fait individuellement. Le déploiement doit se faire sur VM avec Docker. De plus, il est recommandé de compléter la documentation suivante : (Rapport Arc42, ADR, UML) pour la remise.

### 2.3 Conventions
Les tests doivent couvrir les trois niveaux: unitaire, intégration et end-to-end. Chaque fichier contient un header indiquant les UC implémentés pour faciliter la traçabilité.

## 3. Portée et Contexte du Système

### 3.1 Contexte Métier
Le système connecte trois types d'utilisateurs principaux. Les employés de magasin consultent les stocks locaux et déclenchent des demandes de réapprovisionnement. Les gestionnaires de la maison mère supervisent les performances globales et mettent à jour les produits. Les responsables logistiques traitent les flux de marchandises entre le centre et les magasins.

### 3.2 Contexte Technique
Les entrées proviennent des consoles Python et des requêtes HTTP via FastAPI. Les sorties incluent l'affichage console, les réponses JSON et les webhooks. La persistance utilise PostgreSQL via le Repository Pattern. L'infrastructure repose sur des containers Docker déployés sur VM.

### 3.3 Interfaces Externes
PostgreSQL centralise toute la persistance du système multi-magasins et ensuite les webhooks permettent d'envoyer des notifications automatiques d'événements métier vers des systèmes externes. Comme vu ci-bas, les webhooks surveillent automatiquement les niveaux de stock et déclenchent des alertes asynchrones lorsque le stock atteint un seuil critique. Ces notifications JSON sont envoyées instantanément vers la maison mère sans intervention manuelle. C'est un système d'alerte proactif qui permet à la maison mère d'être avertie automatiquement des situations critiques dans les magasins (is_stock_low()).

## 4. Stratégie de Solution

### 4.1 Approche Architecturale
J'ai choisi d'implémenter le Repository Pattern avec injection de dépendances pour découpler la logique métier de l'accès aux données. Cette approche facilite les tests et permet de changer facilement de base de données à l'avenir.

### 4.2 Décisions Stratégiques
PostgreSQL est utilisé exclusivement, éliminant toute simulation pour une implémentation réaliste. Les interfaces ont été simplifiées en intégrant les UC directement dans les interfaces principales plutôt que d'avoir des sous-interfaces imbriquées. La centralisation des instances dans instances.py évite les imports circulaires.

### 4.3 Atteinte Objectifs Qualité
L'évolutivité est assurée par les interfaces repository qui permettent de changer de base de données facilement. La testabilité bénéficie de l'injection de services qui simplifie le mocking. La maintenabilité profite de couches bien séparées avec des responsabilités claires.

## 5. Vue des Blocs de l'architecture

### 5.1 Niveau 1 - Vue d'Ensemble
L'architecture suit une approche en couches classique. La couche interface gère les interactions utilisateur via console et API. La couche service contient toute la logique métier. La couche repository abstrait l'accès aux données. La couche domaine définit les entités métier. PostgreSQL assure la persistance.

### 5.2 Niveau 2 - Services Métier
GestionStocks s'occupe de la consultation du stock central pour UC2. RapportsConsolides génère les rapports de ventes pour UC1. TableauBordService produit le tableau de bord des performances pour UC3. GestionProduitsService gère les mises à jour de produits pour UC4. ReapprovisionnementService traite les demandes pour UC6.

### 5.3 Niveau 3 - Implémentation
PostgreSQLStockRepository accède aux données produites et demandes. PostgreSQLVenteRepository gère les données de ventes et rapports. L'injection de dépendances est centralisée via instances.py pour créer tous les objets nécessaires.

## 6. Vue d'Exécution

### 6.1 UC2: Consultation Stock + Demande Réapprovisionnement
L'employé utilise ConsoleEmployeMagasin qui appelle GestionStocks. Le service consulte StockRepository qui interroge PostgreSQL. Si le stock est faible, une DemandeReapprovisionnement est créée et persistée via StockRepository.

### 6.2 UC6: Traitement Réapprovisionnement
Le responsable logistique utilise InterfaceLogistique pour lister les demandes via ReapprovisionnementService. Après validation du stock disponible via StockRepository, le transfert met à jour les quantités et change le statut à "TRAITE".

### 6.3 UC1: Génération Rapport Consolidé
Le gestionnaire lance la génération via ConsoleGestionnaire qui utilise RapportsConsolides. Le service agrège les ventes via VenteRepository, calcule les métriques par magasin et top produits, puis affiche le rapport formaté.

## 7. Vue de Déploiement

### 7.1 Architecture Conteneurisée
Le docker-compose.yml définit deux services principaux. Le service db utilise postgres:13 avec les variables d'environnement pour lab2_db et lab2_user. Le service app build l'application, expose le port 8000 et dépend du service db.

### 7.2 Environnements
- Développement: Docker Compose local
- Production: VM avec Docker Compose
- Tests: Containers temporaires

### 7.3 Propriétés Déploiement
- Réseau: Bridge Docker interne
- Volumes: Persistance PostgreSQL
- Ports: 8000 (FastAPI), 5432 (PostgreSQL interne)

## 8. Concepts Transversaux

### 8.1 Modèles de Domaine
La classe Produit contient les informations de base (id, nom, prix) et les données de stock (stock_central, seuil_critique). La méthode is_stock_low() détermine si un réapprovisionnement est nécessaire. La classe DemandeReapprovisionnement gère le workflow avec les statuts EN_ATTENTE, APPROUVE, TRAITE ou REJETE.

### 8.2 Patterns Architecturaux
Le Repository Pattern abstrait complètement l'accès aux données. La Dependency Injection est centralisée dans instances.py pour éviter le couplage. La Service Layer isole toute la logique métier. Les Console Interfaces fournissent des points d'entrée spécialisés par type d'utilisateur.

### 8.3 Règles de Conception
Chaque agrégat métier a son repository (StockRepository, VenteRepository). Les services restent stateless sans données persistées. Les interfaces ont été simplifiées en intégrant les UC directement plutôt que d'avoir des sous-menus complexes.

## 9. Décisions d'Architecture

### 9.1 ADR-001: Persistance : PostgreSQL
Le choix entre simulation et vraie persistance était crucial. J'ai opté pour PostgreSQL uniquement en éliminant les fake repositories. Cela apporte plus de réalisme et d'apprentissage mais complique le setup initial.

### 9.2 ADR-002: Interfaces
J'ai intégré les UC directement dans les interfaces principales. La navigation devient plus simple et la maintenance plus facile.

Comme vu ci-bas, le cas d'utilisation UC8 impose une "interface web minimale pour gestionnaires" et la console conservée pour employés magasins (continuité Lab 1) permet une rapidité opérationnelle. De plus, cette séparation des interfaces selon les rôles utilisateurs optimise l'expérience et renforce l'approche DDD.

### 9.3 ADR-003: Patron Repository
Le couplage fort entre logique métier et accès données posait un problème. J'ai implémenté des interfaces repository avec des implémentations PostgreSQL. Cela améliore la testabilité et l'évolutivité mais ajoute une complexité initiale.

## 10. Exigences de Qualité

### 10.1 Performance
L'objectif est d'obtenir une réponse en moins de 2 secondes pour la consultation de stock. Les mesures se font avec des tests simulant 5 magasins simultanés. L'implémentation utilise des requêtes SQL optimisées.

### 10.2 Maintenabilité
Le but est d'ajouter de nouvelles fonctionnalités sans refactoring majeur. La mesure se base sur le temps de développement de nouvelles UC. L'architecture en couches et le Repository Pattern facilitent cet objectif.

### 10.3 Testabilité
La couverture de tests doit dépasser 80% mesurée par pytest coverage. L'injection de dépendances et le mocking des repositories permettent d'atteindre cet objectif.

### 10.4 Évolutivité
Le système doit supporter plus de 10 magasins et des interfaces web/mobile. Les mesures portent sur la performance avec une charge augmentée. L'architecture découplée et l'API REST préparent cette évolution.

## 11. Risques et Dette Technique

### 11.1 Risques Identifiés
PostgreSQL représente un single point of failure critique et la simulation des stocks magasins n'est pas une vraie distribution. La synchronisation concurrentielle reste limitée. Les tests E2E dépendent du démarrage de l'API.

### 11.2 Dette Technique
La gestion d'erreurs reste basique avec des print statements. Cela pourrait engendrer des problèmes de maintenance et délais. Le logging minimal complique le debugging en production, et la validation des données d'entrée est limitée ce qui peut causer des erreurs silencieuses. Certains paramètres restent hardcodés dans le code plutôt que configurés via des variables d'environnement, réduisant la flexibilité du déploiement.

### 11.3 Stratégies d'Atténuation
Un framework de logging structuré comme loguru améliorerait le debugging.

## 12. Glossaire

- Patron Repository : Patron qui encapsule la logique d'accès aux données avec une interface abstraite, permettant de changer d'implémentation facilement.

- Injection de dépendances : Technique qui fournit les dépendances externes via le constructeur plutôt que de les créer directement dans la classe.

- Webhook : Notification HTTP automatique envoyée vers un système externe lors d'événements métier.

- Seuil critique : Niveau de stock minimum qui déclenche une alerte de réapprovisionnement.

---
Version : 1.0  
Date : Juin 2025  
Auteur : Aicha Aanounou  
Cours : LOG430 
