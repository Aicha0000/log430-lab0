-- Script d'initialisation pour Lab 3
-- Base de données simple pour l'API

CREATE TABLE IF NOT EXISTS produits (
    id VARCHAR(10) PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prix DECIMAL(10,2) NOT NULL,
    description TEXT,
    stock_central INTEGER DEFAULT 0,
    seuil_critique INTEGER DEFAULT 10
);

CREATE TABLE IF NOT EXISTS magasins (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    adresse TEXT
);

CREATE TABLE IF NOT EXISTS ventes (
    id SERIAL PRIMARY KEY,
    magasin_id INTEGER REFERENCES magasins(id),
    produit_id VARCHAR(10) REFERENCES produits(id),
    quantite INTEGER NOT NULL,
    prix_unitaire DECIMAL(10,2) NOT NULL,
    date_vente TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Données de test pour l'API
INSERT INTO produits (id, nom, prix, description, stock_central, seuil_critique) VALUES
('P001', 'Ordinateur Portable', 999.99, 'Laptop haute performance', 50, 10),
('P002', 'Souris Sans Fil', 29.99, 'Souris ergonomique', 200, 20),
('P003', 'Clavier Mécanique', 89.99, 'Clavier gaming RGB', 75, 15),
('P004', 'Écran 24"', 299.99, 'Moniteur Full HD', 30, 5),
('P005', 'Webcam HD', 49.99, 'Caméra 1080p', 100, 10);

INSERT INTO magasins (nom, adresse) VALUES
('Magasin Centre-Ville', '123 Rue Principale'),
('Magasin Banlieue', '456 Avenue des Érables'),
('Magasin Mall', '789 Boulevard Commercial'),
('Magasin Campus', '321 Rue Universitaire'),
('Magasin Express', '654 Route Express');

-- Quelques ventes de test
INSERT INTO ventes (magasin_id, produit_id, quantite, prix_unitaire) VALUES
(1, 'P001', 2, 999.99),
(2, 'P002', 5, 29.99),
(1, 'P003', 1, 89.99),
(3, 'P004', 3, 299.99),
(2, 'P005', 2, 49.99);