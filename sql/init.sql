-- Initialisation base de données PostgreSQL

-- Crée la table magasins
CREATE TABLE IF NOT EXISTS stores (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crée la table produits
CREATE TABLE IF NOT EXISTS products (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    central_stock INTEGER DEFAULT 0,
    critical_threshold INTEGER DEFAULT 10,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crée la table ventes
CREATE TABLE IF NOT EXISTS sales (
    id SERIAL PRIMARY KEY,
    store_id VARCHAR(50) REFERENCES stores(id),
    product_id VARCHAR(50) REFERENCES products(id),
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crée la table demandes_réapprovisionnement
CREATE TABLE IF NOT EXISTS replenishment_requests (
    id VARCHAR(100) PRIMARY KEY,
    store_id VARCHAR(50) REFERENCES stores(id),
    product_id VARCHAR(50) REFERENCES products(id),
    requested_quantity INTEGER NOT NULL,
    status VARCHAR(20) DEFAULT 'PENDING',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP
);

-- Insère les 5 magasins
INSERT INTO stores (id, name) VALUES
('magasin 1', 'magasin 1'),
('magasin 2', 'magasin 2'),
('magasin 3', 'magasin 3'),
('magasin 4', 'magasin 4'),
('magasin 5', 'magasin 5')
ON CONFLICT (id) DO NOTHING;

-- Insère les produits initiaux
INSERT INTO products (id, name, description, price, central_stock, critical_threshold) VALUES
('1', 'Coca-Cola', 'Boisson gazeuse classique', 1.99, 150, 10),
('2', 'Snapple', 'Jus de pomme naturel', 2.49, 8, 10),
('3', 'Jus Orange Tropicana', 'Jus orange naturel', 4.99, 45, 10),
('4', 'Sprite', 'Boisson gazeuse citron-lime', 1.99, 120, 10),
('5', 'Frutopia', 'Boisson aux fruits', 2.79, 5, 10)
ON CONFLICT (id) DO NOTHING;

-- Insère les données de vente d'exemple
INSERT INTO sales (store_id, product_id, quantity, unit_price, total_amount, sale_date) VALUES
('magasin 1', '1', 10, 1.99, 19.90, CURRENT_TIMESTAMP - INTERVAL '1 day'),
('magasin 1', '2', 5, 2.49, 12.45, CURRENT_TIMESTAMP - INTERVAL '1 day'),
('magasin 2', '1', 15, 1.99, 29.85, CURRENT_TIMESTAMP - INTERVAL '2 days'),
('magasin 2', '3', 8, 4.99, 39.92, CURRENT_TIMESTAMP - INTERVAL '2 days'),
('magasin 3', '4', 12, 1.99, 23.88, CURRENT_TIMESTAMP - INTERVAL '3 days')
ON CONFLICT DO NOTHING;

-- Crée les index pour la performance
CREATE INDEX IF NOT EXISTS idx_sales_store_date ON sales(store_id, sale_date);
CREATE INDEX IF NOT EXISTS idx_sales_product ON sales(product_id);
CREATE INDEX IF NOT EXISTS idx_replenishment_status ON replenishment_requests(status);
CREATE INDEX IF NOT EXISTS idx_products_stock ON products(central_stock);

-- Crée la vue pour les alertes de stock bas
CREATE OR REPLACE VIEW low_stock_view AS
SELECT 
    id,
    name,
    central_stock,
    critical_threshold,
    (central_stock <= critical_threshold) as is_low_stock,
    CASE 
        WHEN central_stock <= critical_threshold THEN 'stock faible'
        ELSE 'stock normal'
    END as severity
FROM products
WHERE central_stock <= critical_threshold;

-- Fonction pour update timestamp produit automatiquement
CREATE OR REPLACE FUNCTION update_product_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger pour update automatique timestamp quand produit modifié
CREATE TRIGGER update_product_timestamp_trigger
    BEFORE UPDATE ON products
    FOR EACH ROW
    EXECUTE FUNCTION update_product_timestamp();

-- Accorde les permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO lab3_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO lab3_user;
