# Analyse et Continuité pour le labo 2
- Évolution vers une Architecture multi-magasins

# 1. Résumez clairement les solutions développées aux Labs 0 et 1
 ## Labo 0: 
 Mise en place de l'infrastructure de développement et d'une app minimale

# Réalisations:
- Appplication Python minimale avec un message de sortie
- Conteneurisation avec Docker, Dockerfile et utilisation de docker-compose.yml
- Tests unitaires avec Pytest
- Pipeline CI/CD complète sur Github Actions
- Documentation complète dans README.md
- Structure de lab claire et égitignore approprié

**Technologies choisies :**  Python, Docker, Docker compose, Github Actions, Pytest

## Lab 1:
Développement d'un système de caisse pour un magasin de quartier 

# Réalisations:
- Architecture client/serveur 2-tier (application console + base de données)
- Application console permettant: Recherche de produits par ID, nom; Enregistrement des Ventes, Gestion des retours, Consultation des stocks
- Couche de persistance abstraite avec ORM
- Support de 3 caises simultanées avec gestion des transactions
- Documentation technique avec diagrammes UML (modèle 4+1)
- 2 ADRs
- Continuation de la pipeline CI/CD du labo 0

**Architecture:** Système mono-magasin avec accès direct à une base de données locale

# 2. Les éléments à conserver, modifier ou refactorer
 ** À conserver:
 - Pipeline CI/CD complète (GitHub Actions)
 - Conteneurisation Docker + Docker Compose
 - Documentation technique et ADRs
 - Logique de vente et calcul des totaux
 - Abstraction de la couche de persistance (ORM)
- Tests automatisés

** À changer:
- Passage du 2-tier vers une architecture distribuée
- Gestion multi-magasins au lieu d'un seul point de vente
- Synchronisation des données entre magasins
- Support de nouveaux types d'utilisateurs :
  - Employés de magasin (existant, à étendre)
  - Gestionnaires maison mère (nouveau)
  - Responsables logistique (nouveau)
- Nouvelles fonctionnalités d'interface selon les rôles

** À refactorer:
- Connexion directe et unique à une base de données locale
- Architecture centrée sur un seul point de vente
- Pas de gestion des rôles utilisateurs différenciés

# 3. Les nouvelles exigences et les défis architecturaux
** Besoins fonctionnels:
- 5 magasins au lieu de un seul
- 1 centre de logistique
- 1 maison mère (administration)

** Nouveaux cas d'utilisations:
- UC1 : Génération de rapports consolidés des ventes (maison mère)
- UC2 : Consultation du stock central + demandes de réapprovisionnement
- UC3 : Tableau de bord des performances multi-magasins
- UC4 : Mise à jour centralisée des produits depuis la maison mère
- UC6 : Approvisionnement des magasins depuis le centre logistique
- UC7 : Alerter automatiquement la maison mère en cas de rupture
critique
- UC8 : Offrir une interface web minimale pour les gestionnaires
  
** Défis architecturaux identifiés pour l'instant:
- Synchronisation des stocks entre magasins et entrepôt
- Assurer la cohérence des prix et informations produits en temps réel
- Mettre en place une base de donnée qui permet l'autonomie des magasins
- Pouvoir supporter la charge de 5 magasins simultanément

## 4. Introduisez une réflexion basée sur les principes du Domain-Driven Design (DDD) 
** Sous-domaines fonctionnels identifiés:
* Ventes en magasin:
- Gestion des transactions de vente
- Calcul des totaux 
- Gestion des retours
- Interface caisse pour employés

* Gestion logistique
- Gestion du stock central (entrepôt)
- Traitement des demandes de réapprovisionnement
- Planification et exécution des livraisons
- Suivi des transferts de stock
- Alertes de rupture de stock

* Supervision et administration
- Génération de rapports consolidés
- Tableaux de bord multi-magasins
- Gestion centralisée des produits (prix, descriptions)
- Indicateurs de performance des magasins
- Administration des utilisateurs et magasins

DDD:
- Context Magasin : Ventes locales, stock local, employés
- Context Logistique : Entrepôt, réapprovisionnement, transferts
- Context Administration : Rapports, configuration, supervision
