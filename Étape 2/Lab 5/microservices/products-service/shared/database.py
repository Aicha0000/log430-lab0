import os
import psycopg2
from psycopg2.extras import RealDictCursor

class DatabaseConfig:
    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL")
    
    def get_connection(self):
        return psycopg2.connect(
            self.database_url,
            cursor_factory=RealDictCursor
        )

class BaseRepository:
    def __init__(self, db_config: DatabaseConfig):
        self.db_config = db_config
    
    def execute_query(self, query: str, params=None):
        conn = self.db_config.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        
        if cursor.description:
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return [dict(row) for row in result]
        else:
            conn.commit()
            cursor.close()
            conn.close()
            return None
    
    def execute_one(self, query: str, params=None):
        conn = self.db_config.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return dict(result) if result else None

def setup_tables(db_config):
    products_sql = """
    CREATE TABLE IF NOT EXISTS products (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        description TEXT,
        price DECIMAL(10,2) NOT NULL,
        category VARCHAR(100),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    customers_sql = """
    CREATE TABLE IF NOT EXISTS customers (
        id SERIAL PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        first_name VARCHAR(100) NOT NULL,
        last_name VARCHAR(100) NOT NULL,
        phone VARCHAR(20),
        address TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    orders_sql = """
    CREATE TABLE IF NOT EXISTS orders (
        id SERIAL PRIMARY KEY,
        customer_id INTEGER NOT NULL,
        status VARCHAR(20) DEFAULT 'pending',
        total_amount DECIMAL(10,2) NOT NULL,
        store_id VARCHAR(100),
        delivery_address TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    inventory_sql = """
    CREATE TABLE IF NOT EXISTS inventory (
        id SERIAL PRIMARY KEY,
        product_id VARCHAR(100) NOT NULL,
        store_id VARCHAR(100) NOT NULL,
        quantity INTEGER NOT NULL,
        reserved INTEGER DEFAULT 0
    );
    """
    
    sales_sql = """
    CREATE TABLE IF NOT EXISTS sales (
        id SERIAL PRIMARY KEY,
        product_id VARCHAR(100) NOT NULL,
        store_id VARCHAR(100) NOT NULL,
        quantity INTEGER NOT NULL,
        unit_price DECIMAL(10,2) NOT NULL,
        sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    reports_sql = """
    CREATE TABLE IF NOT EXISTS reports (
        id SERIAL PRIMARY KEY,
        report_type VARCHAR(100) NOT NULL,
        data TEXT,
        generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    cart_sql = """
    CREATE TABLE IF NOT EXISTS cart_items (
        id SERIAL PRIMARY KEY,
        user_id VARCHAR(100) NOT NULL,
        product_id VARCHAR(100) NOT NULL,
        quantity INTEGER NOT NULL,
        added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    checkout_sql = """
    CREATE TABLE IF NOT EXISTS checkout_sessions (
        id SERIAL PRIMARY KEY,
        user_id VARCHAR(100) NOT NULL,
        status VARCHAR(50) DEFAULT 'pending',
        total_amount DECIMAL(10,2),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    conn = db_config.get_connection()
    cursor = conn.cursor()
    
    tables = [products_sql, customers_sql, orders_sql, inventory_sql, 
              sales_sql, reports_sql, cart_sql, checkout_sql]
    
    for table_sql in tables:
        cursor.execute(table_sql)
    
    conn.commit()
    cursor.close()
    conn.close()
