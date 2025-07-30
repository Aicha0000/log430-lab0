# Rapport d'Architecture Arc42 - Laboratoire 5
## Architecture Microservices avec API Gateway

---

## 1. Exigences et objectifs

### 1.1 Aperçu des exigences

Ce Laboratoire constitue l'aboutissement logique de l'évolution architecturale amorcée dans les laboratoires précédents. Partant du système multi-magasins développé au Lab 3 et optimisé au Lab 4 avec load balancing et cache, l'objectif principal consiste à décomposer cette architecture monolithique en 8 microservices indépendants tout en intégrant des capacités ecommerce modernes. 

L'exigence fondamentale impose la transformation du système existant en une architecture orientée microservices. Cette décomposition doit respecter les principes de séparation des responsabilités établis lors des laboratoires antérieurs, notamment la distinction entre les opérations du magasin physique et celles de la boutique en ligne. La stratégie retenue extrait 4 services des domaines métier du Lab 4 (products, inventory, sales, reports) et ajoute 4 nouveaux services dédiés à l'e-commerce (customers, orders, cart, checkout).

Le système résultant doit maintenir l'ensemble des fonctionnalités existantes tout en ajoutant les capacités de gestion de comptes clients, de panier d'achat avec load balancing sur 3 instances, et de validation de commandes. L'architecture doit également préserver les mécanismes d'observabilité mis en place au Lab 4, permettant ainsi une comparaison objective des performances entre l'ancienne et la nouvelle architecture. Une attention particulière est portée au cart-service qui démontre les capacités de scaling horizontal requis par l'énoncé du laboratoire.

### 1.2 Objectifs de qualité

L'architecture microservices vise principalement l'amélioration de la scalabilité et de la maintenabilité du système. Chaque service doit pouvoir évoluer indépendamment, permettant aux équipes de développement de travailler en parallèle sans interférences. Cette indépendance s'étend également au déploiement, chaque microservice devant être déployable individuellement sans impact sur les autres composants du système.

La résilience constitue un autre objectif critique. L'architecture doit garantir qu'une défaillance dans un service n'entraîne pas l'arrêt complet du système. Cette isolation des pannes, combinée à des mécanismes de circuit breaker et de fallback, assure la continuité de service même en cas de problèmes ponctuels.

Les performances constituent également un enjeu majeur. Bien que l'introduction d'une API Gateway ajoute une couche supplémentaire de latence, l'architecture distribuée doit compenser cette overhead par une meilleure utilisation des ressources et la possibilité de scaling horizontal sélectif selon les besoins de chaque service.

### 1.3 Parties prenantes

Les parties prenantes incluent principalement les équipes de développement qui bénéficient de la séparation claire des responsabilités et de la possibilité de travailler sur des domaines métier distincts. Cette approche permet un troubleshooting plus précis et des optimisations ciblées.

Les utilisateurs finaux, qu'ils soient clients de l'ecommerce ou employés du magasin physique, attendent une expérience transparente où la complexité architecturale reste invisible. Les administrateurs système requièrent des outils de monitoring consolidés malgré la distribution des services, d'où l'importance de maintenir une stack d'observabilité centralisée.

---

## 2. Contraintes

### 2.1 Contraintes techniques

L'architecture microservices impose plusieurs contraintes techniques spécifiques. La conteneurisation via Docker demeure obligatoire, chaque microservice devant être packagé dans son propre conteneur avec ses dépendances isolées. Cette approche garantit la reproductibilité des déploiements, mais impose une gestion rigoureuse des versions et des configurations, notamment à l'aide de variables d'environnement.

Le principe « database per service » constitue une contrainte architecturale majeure, où 8 bases de données PostgreSQL sont dédiées à un service spécifique (avec cart-db partagée entre 3 instances). Cette isolation des données garantit l'indépendance des services, mais complexifie la gestion des transactions distribuées et nécessite la mise en place de stratégies de cohérence éventuelle. Une exception notable concerne le cart-service, qui utilise 3 instances applicatives partageant une seule base cart-db, illustrant ainsi le pattern de load balancing horizontal, tout en maintenant la cohérence des données de panier entre les instances.

L'instrumentation Prometheus est également obligatoire pour chaque service, assurant la continuité du monitoring mis en place au Laboratoire 4. Cette contrainte impose l'exposition d'un endpoint /metrics standardisé sur chaque microservice, ainsi qu'une collecte centralisée via une instance Prometheus partagée. Les métriques collectées doivent permettre de comparer les performances entre l'architecture monolithique et l'architecture microservices, y compris la mesure de l'impact du load balancing sur les temps de réponse.

### 2.2 Contraintes organisationnelles

Les seules contraintes de type organisationnelles sont concernant la documentation qui doit suivre le format Arc42 et inclure les choix techniques majeurs de l'architecture, ainsi que des captures d'écrans démontrant la progression de chaque étape du laboratoire.

### 2.3 Contraintes d'environnement

Les ports d'exposition suivent une convention stricte avec Kong sur le port 8000 pour le trafic applicatif et 8001 pour l'administration, tandis que chaque microservice expose ses ports internes selon une numérotation séquentielle (8001-8008). Cette organisation facilite le debugging et évite les conflits de ports. Le cart-service est répliqué sur 3 instances pour load balancing round-robin via Kong upstream, où seule la première instance expose le port 8008 externalement, les autres instances étant accessibles uniquement via le load balancer interne.

La compatibilité avec les outils de test existants (k6, JMeter) doit être maintenue pour permettre la comparaison des performances. Les scripts de test du Lab 4 nécessitent des adaptations pour cibler l'API Gateway plutôt que les services directs, avec des scénarios spécifiques testant à la fois les appels via Gateway et les appels directs aux services. Cette double approche permet d'évaluer l'overhead introduit par l'API Gateway et l'efficacité du load balancing sur le cart-service.

---

## 3. Contexte et périmètre du système

### 3.1 Contexte métier

L'architecture existante du Lab 4, bien qu'optimisée en termes de performances avec load balancing et cache, présentait des limitations pour supporter cette évolution métier. Le couplage entre les différents domaines fonctionnels rendait difficile l'innovation rapide sur les aspects ecommerce sans risquer d'impacter les opérations critiques du magasin physique.

La décomposition en microservices répond à ce besoin d'agilité métier en permettant aux équipes de développer et déployer indépendamment les fonctionnalités ecommerce tout en maintenant la stabilité des systèmes de gestion du magasin physique. Cette séparation facilite également l'évolution technologique différenciée selon les besoins spécifiques de chaque domaine.

### 3.2 Contexte technique

L'architecture technique hérite des acquis du Laboratoire 4 en termes d'observabilité et de patterns de résilience, tout en introduisant Kong comme point d'entrée unique pour l'ensemble des microservices. Cette API Gateway centralise la gestion du routage, de la sécurité et du load balancing, simplifiant l'interface externe tout en permettant une complexité interne qui reste maîtrisée.

Le stack technologique reste cohérent avec FastAPI pour les microservices, PostgreSQL pour la persistance et Prometheus/Grafana pour l'observabilité. Cette continuité technologique facilite la migration depuis l'architecture monolithique et capitalise sur l'expertise développée lors des laboratoires précédents.

L'introduction du concept "database per service" constitue l'évolution technique la plus significative, chaque microservice disposant de sa propre instance PostgreSQL. Cette approche garantit l'isolation des données et l'indépendance des schémas.

---

## 4. Stratégie de solution

### 4.1 Approche architecturale

L'approche architectural était la décomposition basée sur les domaines métier identifiés du laboratoire 4. Plutôt qu'une refactorisation complète, la stratégie consiste à extraire intelligemment ou logiquement les services du monolithe existant tout en ajoutant les capacités ecommerce comme nouveaux microservices. Cette transition progressive où les services extraits conservent leurs interfaces et leur logique métier, minimisant les risques de régression. Les nouveaux services ecommerce s'intègrent naturellement dans cet écosystème en utilisant les mêmes patterns techniques et en partageant certains services communs comme l'inventaire.

### 4.2 Décisions d'architecture clés

La décision de retenir Kong comme API Gateway repose sur sa maturité et ses capacités avancées de routage dynamique, de load balancing natif et de plugins d'observabilité. Contrairement à des solutions plus simples comme NGINX, Kong offre une interface d'administration complète et une persistance de configuration dans PostgreSQL, facilitant la gestion opérationnelle. Sa capacité à gérer des upstreams avec health checks automatiques s'avère particulièrement pertinente pour le load balancing du cart-service.

Le choix du pattern "database per service" constitue une décision architecturale fondamentale qui privilégie l'autonomie des services au détriment de la simplicité transactionnelle. Cette approche impose l'adoption de patterns de cohérence éventuelle et de compensation pour gérer les transactions distribuées. L'exception contrôlée du cart-service, où 3 instances partagent cart-db, démontre que ce pattern peut être adapté selon les besoins spécifiques de load balancing tout en maintenant l'isolation des données entre domaines métier.

L'organisation en domaines respecte la séparation naturelle entre les operations du magasin physique (products, inventory, sales, reports) et les fonctionnalités ecommerce (customers, orders, cart, checkout). Cette séparation claire facilite l'évolution indépendante de chaque domaine et permet une spécialisation des équipes de développement. Le cart-service bénéficie d'un load balancing avec 3 instances pour répondre aux exigences de scalabilité du lab et démontrer les capacités de l'architecture distribuée.

---

## 5. Vue d'ensemble de l'architecture

### 5.1 Diagramme d'architecture générale

L'architecture générale s'articule autour de Kong API Gateway qui centralise l'accès à 8 microservices indépendants, avec cart-service déployé en 3 instances load-balancées pour démontrer les capacités de scaling horizontal. Chaque service dispose de sa propre base de données PostgreSQL, à l'exception du cart-service dont les 3 instances partagent une cart-db commune pour maintenir la cohérence des données de panier. Cette organisation garantit l'isolation complète des domaines métier tout en maintenant une interface unifiée pour les clients.

Le flux de données traverse systématiquement Kong qui route les requêtes selon les préfixes de path (/api/products, /api/cart, /api/checkout, etc.) vers les services appropriés ou vers l'upstream load-balancé dans le cas du cart-service. Cette centralisation simplifie la gestion des aspects transversaux comme l'authentification, le rate limiting et l'observabilité au niveau de la gateway. Le monitoring Prometheus collecte les métriques de chaque instance, permettant une visibilité complète sur la distribution de charge et les performances comparatives entre approches directe et via Gateway.

### 5.2 Décomposition en microservices

La décomposition résulte en 8 microservices organisés selon deux catégories principales. Les services hérités du Lab 4 incluent products-service pour la gestion du catalogue de boissons, inventory-service pour le suivi des stocks, sales-service pour les ventes en magasin et reports-service pour l'analyse des performances. Cette extraction respecte la séparation des domaines métier identifiés dans l'architecture monolithique précédente.

Les nouveaux services e-commerce comprennent customers-service pour la gestion des comptes clients, orders-service pour le traitement des commandes, cart-service pour la gestion des paniers d'achat avec persistence temporaire, et checkout-service pour la validation des commandes. Cette organisation respecte les responsabilités métier tout en évitant le couplage excessif entre les fonctionnalités magasin physique et e-commerce.

Le cart-service bénéficie d'une architecture load-balancée avec 3 instances partageant une base de données commune, démontrant les capacités de scaling horizontal requis par l'énoncé du laboratoire. Cette configuration illustre comment l'architecture microservices peut adapter ses patterns selon les besoins spécifiques de performance et de disponibilité de chaque service.

---

## 6. Vue d'exécution

### 6.1 Scénarios d'exécution

Le scénario d'exécution typique d'une commande e-commerce illustre parfaitement les interactions entre microservices dans cette architecture distribuée. Le processus débute par l'authentification du client via customers-service, suivi de la consultation du catalogue via products-service et de la vérification de disponibilité via inventory-service. Ces interactions démontrent la séparation claire des responsabilités où chaque service maintient sa spécialisation métier.

L'ajout d'articles au panier implique cart-service qui maintient l'état temporaire de la session d'achat, avec load balancing automatique entre les 3 instances via Kong Gateway. La finalisation passe par checkout-service qui orchestre la validation de la commande, la réservation du stock via inventory-service et la création de l'ordre via orders-service. Ce workflow démontre comment l'architecture distribuée maintient la cohérence métier malgré la séparation physique des services.

Les scénarios de gestion du magasin physique suivent des patterns plus simples avec des interactions directes entre sales-service et inventory-service pour les ventes en magasin, ou entre reports-service et les différents services pour la génération de rapports consolidés. Cette simplicité relative illustre l'avantage de la séparation entre les domaines métier traditionnels et les nouveaux besoins e-commerce.

### 6.2 Flux de données

Les flux de données transitent systématiquement par Kong Gateway qui agit comme un reverse proxy intelligent. Chaque requête entrante est analysée selon son path (/api/products, /api/cart, /api/checkout, etc.) pour déterminer le service de destination approprié. Kong maintient également des métriques de routage et implémente des stratégies de load balancing pour le cart-service disposant de 3 instances.

La communication inter-services reste synchrone via HTTP/REST pour maintenir la simplicité et la cohérence avec l'architecture existante. Cette approche évite la complexité des systèmes de messaging asynchrone tout en permettant des optimisations futures comme la mise en cache au niveau de Kong ou l'implémentation de circuit breakers.

Les données de monitoring suivent un flux parallèle avec chaque service exposant ses métriques Prometheus qui sont collectées centralement. Cette observabilité distribuée permet un monitoring fin de chaque composant, incluant la distribution de charge entre les instances du cart-service, tout en maintenant une vue d'ensemble via Grafana.

---

## 7. Vue de déploiement

### 7.1 Infrastructure

L'infrastructure de déploiement repose entièrement sur Docker Compose orchestrant 23 conteneurs répartis en services applicatifs, bases de données et outils de monitoring. Cette approche garantit l'isolation des processus et la reproductibilité des environnements tout en conservant la simplicité d'un déploiement local adapté au contexte pédagogique.

Chaque microservice est packagé dans son propre conteneur avec un Dockerfile dédié incluant les dépendances Python spécifiques. Les images sont construites localement à partir du code source, permettant des cycles de développement rapides et une personnalisation fine de chaque service. Le cart-service est répliqué en 3 instances identiques pour démontrer les capacités de load balancing.

Les bases de données PostgreSQL sont déployées comme services indépendants avec volumes persistants pour garantir la durabilité des données entre les redémarrages. 8 bases de données respectent le principe d'isolation, avec une exception contrôlée pour cart-db partagée entre les 3 instances du cart-service pour maintenir la cohérence des données de panier.

### 7.2 Mapping des composants

Le mapping des composants suit une convention de ports stricte facilitant le développement et le debugging. Kong occupe les ports 8000 pour le trafic applicatif et 8001 pour l'administration, devenant le point d'entrée unique pour toutes les interactions externes. Cette centralisation simplifie l'interface client tout en cachant la complexité de l'architecture distribuée.

Les microservices utilisent des ports externes mappés (8002-8009) correspondant aux ports internes (8001-8008) avec mapping externe for l'accès direct en mode développement. Seule la première instance du cart-service expose le port 8008 externalement, les autres instances étant accessibles uniquement via le load balancer Kong. Cette configuration permet de tester les services individuellement tout en validant le routage via Kong Gateway.

Les outils de monitoring conservent leurs ports standards avec Prometheus sur 8010 et Grafana sur 8011, évitant les conflits avec d'éventuelles instances existantes et facilitant l'intégration avec des outils externes de monitoring. Cette stabilité des points d'accès facilite la comparaison avec l'architecture du Lab 4.

---

## 8. Concepts transversaux

### 8.1 Sécurité

La sécurité de l'architecture microservices s'articule autour de Kong Gateway qui centralise les contrôles d'accès et peut implémenter des stratégies d'authentification unifiées. La configuration actuelle inclut la gestion CORS via un script dédié (setup-kong-cors.sh) pour permettre l'accès depuis des clients web, démontrant la flexibilité de Kong pour gérer les aspects de sécurité transversaux.

L'isolation réseau entre les services est assurée par les réseaux Docker dédiés (kong-net et microservices-net), limitant les communications aux seuls échanges nécessaires. Cette segmentation réduit la surface d'attaque et facilite l'implémentation de politiques de sécurité granulaires au niveau réseau.

La sécurité des données bénéficie du principe "database per service" qui isole naturellement les données sensibles et permet l'implémentation de politiques de chiffrement et d'accès différenciées selon les exigences de chaque domaine métier. L'exception du cart-service avec base partagée maintient l'isolation des domaines tout en optimisant les performances du load balancing.

### 8.2 Monitoring et observabilité

L'observabilité de l'architecture distribuée s'appuie sur la continuité de la stack Prometheus/Grafana établie au Lab 4, enrichie par les métriques Kong Gateway. Chaque microservice expose un endpoint /metrics standardisé collectant les métriques de performance, d'erreurs et de throughput, incluant les 3 instances du cart-service pour analyser la distribution de charge.

Kong ajoute une dimension supplémentaire d'observabilité en fournissant des métriques de routage, de latence au niveau gateway et de distribution de charge entre les instances du cart-service. Cette visibilité centralisée facilite l'identification des goulots d'étranglement et l'optimisation des performances globales, particulièrement critique pour évaluer l'efficacité du load balancing.

La corrélation entre les métriques des différents services permet d'analyser les flux de bout en bout et d'identifier les dépendances critiques. Cette approche d'observabilité distribuée maintient la visibilité opérationnelle malgré la complexité architecturale accrue, avec des outils de test K6 et JMeter permettant la comparaison entre appels directs et via Gateway.

### 8.3 Gestion des erreurs

La gestion des erreurs dans l'architecture microservices adopte une approche de resilience patterns avec isolation des pannes au niveau de chaque service. Chaque microservice implémente ses propres mécanismes de gestion d'erreur et expose des endpoints de health check permettant à Kong de détecter les services défaillants, particulièrement important pour le load balancing du cart-service.

Les erreurs de communication inter-services sont gérées par des timeouts configurables et des réponses HTTP standardisées permettant aux clients de distinguer les erreurs temporaires des erreurs permanentes. Cette stratégie facilite l'implémentation de logiques de retry côté client et améliore la résilience globale du système distribué.

Kong peut également implémenter des circuit breakers pour protéger les services downstream des cascades de pannes, bien que cette fonctionnalité ne soit pas activée dans l'implémentation actuelle. Le health checking automatique des instances du cart-service illustre les fondations nécessaires pour ces patterns de résilience avancés.

### 8.4 Communication inter-services

La communication inter-services privilégie HTTP/REST synchrone pour maintenir la simplicité et la cohérence avec les patterns établis au Lab 4. Cette approche évite la complexité des systèmes de messaging asynchrone tout en conservant une intégration naturelle avec les outils de monitoring HTTP existants et les capacités de load balancing de Kong.

Les contrats d'interface entre services sont définis via les APIs REST avec documentation automatiquement générée par FastAPI. Cette standardisation facilite la découverte des services et la génération de clients automatisés pour les tests d'intégration, particulièrement utile pour tester les interactions avec les multiples instances du cart-service.

La découverte de services s'appuie sur la résolution DNS Docker et les noms de services statiques définis dans docker-compose.yml. Cette approche simple évite la complexité d'un service registry dédié tout en maintenant la flexibilité nécessaire pour l'environnement de développement. Kong gère automatiquement le routage vers les instances appropriées via son système d'upstream.

---

## 9. Décisions d'architecture

### 9.1 ADR-001 : Architecture Microservice

**Contexte :** Le système monolithique du Lab 4 limite la scalabilité et l'agilité de développement nécessaires pour les évolutions e-commerce tout en maintenant les opérations du magasin physique.

**Décision :** Décomposition en 8 microservices avec database per service pattern.

**Justification :** Cette architecture permet l'évolution indépendante des domaines métier, facilite le scaling horizontal sélectif et améliore la résilience par isolation des pannes. La séparation magasin physique/e-commerce reflète naturellement les besoins métier identifiés.

**Conséquences :** Complexité opérationnelle accrue avec 23 conteneurs à gérer, défis de cohérence des données transactionnelles, mais gain significatif en flexibilité et maintenabilité. L'architecture préserve les investissements existants tout en ouvrant de nouvelles possibilités d'innovation.

### 9.2 ADR-002 : Kong API Gateway et Point d'entrée unique

**Contexte :** Les 8 microservices nécessitent un point d'entrée unifié pour le routage, l'authentification et l'observabilité centralisée.

**Décision :** Implémentation de Kong Gateway comme API Gateway unique sur le port 8000 avec routage par path (/api/products, /api/cart, etc.).

**Justification :** Kong offre le routage centralisé, la gestion CORS, les plugins de sécurité et l'interface d'administration. Simplifie l'intégration client avec un seul endpoint et permet l'observabilité centralisée.

**Conséquences :** Point d'entrée unique simplifie les intégrations client, observabilité centralisée et gestion des cross-cutting concerns, mais introduction d'un point de défaillance unique et latence additionnelle.

### 9.3 ADR-003 : Load Balancing du Cart Service

**Contexte :** Les microservices nécessitent une distribution intelligente du trafic avec des capacités de health checking et de failover automatique pour répondre aux exigences du laboratoire.

**Décision :** Implémentation du load balancing round-robin pour cart-service avec 3 instances via Kong Gateway upstream.

**Justification :** Kong offre des fonctionnalités avancées de routage dynamique, de gestion des upstreams et d'observabilité intégrée. Le cart-service est choisi comme candidat optimal car ses opérations sont largement stateless avec base dedonnées partagée.

**Conséquences :** Latence légèrement supérieure due aux health checks Kong, mais gain substantiel en résilience et capacités de scaling. L'interface d'administration simplifie la gestion des routes et permet l'observation de la distribution de charge.

---

## 10. Exigences de qualité

### 10.1 Performance

Les performances de l'architecture microservices montrent des résultats contrastés par rapport au Lab 4. Les tests de charge révèlent une latence moyenne variable selon la complexité des services, avec Kong Gateway introduisant un overhead moyenne de 15.65ms par requête, compensée par ses capacités de load balancing qui permettent une distribution efficace du trafic entre les 3 instances du cart-service.

**Analyse des Résultats :**
- Latence moyenne directe: 5.47ms
- Latence moyenne via Gateway: 21.12ms
- Première requête: Impact significatif (+81ms) dû à l'initialisation des connexions Kong
- Requêtes suivantes: Overhead minimal (<1ms) grâce à la réutilisation des connexions

Une observation importante à soulever est que le premier appel via Gateway présente une latence significativement plus élevée (88ms vs 7ms) due à l'établissement initial des connexions et à l'initialisation des routes Kong. Les appels subséquents montrent des performances comparables, démontrant l'efficacité du pooling de connexions de Kong.

### 10.2 Scalabilité

La scalabilité constitue l'un des bénéfices majeurs de l'architecture microservices. Chaque service peut être scalé horizontalement indépendamment selon ses besoins spécifiques, permettant une allocation optimale des ressources. Le cart-service démontre cette capacité avec trois instances configurées derrière Kong pour gérer les pics de charge e-commerce selon les exigences du laboratoire.

La stratégie de scaling sélectif permet de concentrer les ressources sur les services les plus sollicités sans impacter les autres composants. Cette approche contraste favorablement avec le scaling monolithique du Lab 4 qui nécessitait la duplication complète de l'application même pour des besoins partiels.

### 10.3 Disponibilité

La disponibilité bénéficie grandement de l'isolation des services qui limite l'impact des pannes individuelles. Une défaillance d'une instance du cart-service n'affecte pas les opérations du magasin physique gérées par sales-service, démontrant la résilience de l'architecture compartimentée avec load balancing automatique.

Kong Gateway inclut des mécanismes de health checking qui détectent automatiquement les services défaillants et redirigent le trafic vers les instances saines du cart-service. Cette capacité améliore significativement la disponibilité perçue par les utilisateurs, même en cas de pannes partielle d'instances individuelles.

### 10.4 Maintenabilité

La maintenabilité constitue l'un des bénéfices les plus significatifs de l'architecture microservices. Chaque service dispose de sa propre base de code, de ses tests et de ses cycles de déploiement indépendants, facilitant la parallélisation du développement et réduisant les risques de régression inter-équipes.

L'isolation des responsabilités simplifie la compréhension du code et accélère l'onboarding des nouveaux développeurs qui peuvent se concentrer sur un domaine métier spécifique. Le load balancing du cart-service illustre comment les patterns de scalabilité peuvent être appliqués de manière ciblée sans complexifier l'ensemble du système.

---

## 11. Dettes techniques

La dette technique principale de l'architecture actuelle concerne l'absence de gestion transactionnelle distribuée. Les opérations impliquant plusieurs services, comme la finalisation d'une commande qui affecte inventory-service, cart-service et orders-service, reposent sur des appels séquentiels sans garantie de cohérence en cas d'échec partiel.

L'implémentation actuelle du cart-service utilise un stockage en mémoire qui ne survit pas aux redémarrages des instances. Cette limitation nécessite une évolution vers une persistence appropriée dans cart-db, idéalement avec expiration automatique des paniers abandonnés pour éviter l'accumulation de données obsolètes entre les 3 instances.

La configuration Kong reste largement manuelle via des scripts shell (setup-kong.sh, setup-kong-cors.sh, setup-kong-loadbalancing.sh), créant un risque d'inconsistance et compliquant les déploiements automatisés. L'évolution vers une approche Infrastructure as Code améliorerait significativement la reproductibilité et la fiabilité des déploiements.

L'absence de circuit breakers et de retry policies au niveau applicatif expose le système aux cascades de pannes et aux timeouts en chaîne. L'implémentation de ces patterns de résilience, soit au niveau Kong soit dans chaque service, améliorerait substantiellement la robustesse globale du système distribué.

---

## 12. Conclusion

Le Laboratoire 5 démontre avec succès la faisabilité et les bénéfices d'une architecture microservices pour un système e-commerce moderne. La décomposition intelligente du monolithe du Lab 4 en 8 services spécialisés illustre comment préserver les investissements existants tout en créant les fondations pour une innovation continue.

L'architecture résultante offre une flexibilité sans précédent pour l'évolution indépendante des domaines métier, particulièrement critique pour la séparation entre les opérations du magasin physique et les exigences e-commerce. Cette séparation facilite l'innovation rapide sur les aspects numériques sans risquer de perturber les opérations critiques du commerce de détail.

Kong Gateway prouve sa valeur comme point d'orchestration central, simplifiant l'interface externe tout en préservant la complexité interne nécessaire à la flexibilité architecturale. Ses capacités de load balancing démontrées avec le cart-service, de monitoring et de gestion de politiques centralisées compensent largement l'overhead de latence introduit.

L'observabilité distribuée maintient la visibilité opérationnelle essentielle, démontrant que la complexité architecturale n'implique pas nécessairement une perte de contrôle opérationnel. La continuité des outils de monitoring facilite la comparaison objective avec l'architecture précédente et guide les optimisations futures.

Cette transformation architecturale constitue un investissement stratégique pour l'avenir, créant les fondations techniques nécessaires pour supporter la croissance e-commerce tout en maintenant l'excellence opérationnelle du commerce traditionnel. Les défis identifiés, notamment autour de la cohérence transactionnelle et de la résilience, représentent les prochaines étapes naturelles d'évolution plutôt que des limitations fondamentales de l'approche microservices adoptée.

## 13. UML
diagrammes sous /docs/uml