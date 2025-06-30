"""
PostgreSQL implementation de VenteRepository
"""
import psycopg2
from typing import List, Dict
from datetime import datetime, timedelta
from collections import defaultdict
import os

from commun.repositories.vente_repository import VenteRepository
from commun.modeles.vente import Vente


class PostgreSQLVenteRepository(VenteRepository):
    """Real PostgreSQL implementation for sales data"""
    
    def __init__(self):
        self.connection_string = os.getenv(
            "DATABASE_URL", 
            "postgresql://user:password@localhost:5432/lab2_db"
        )
        self._init_tables()
    
    def _get_connection(self):
        """Get database connection"""
        return psycopg2.connect(self.connection_string)
    
    def _init_tables(self):
        """Create sales table if it doesn't exist"""
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS ventes (
                        id VARCHAR PRIMARY KEY,
                        magasin_id VARCHAR NOT NULL,
                        produit_id VARCHAR NOT NULL,
                        quantite INTEGER NOT NULL,
                        prix_unitaire DECIMAL(10,2) NOT NULL,
                        total DECIMAL(10,2) NOT NULL,
                        date_vente TIMESTAMP NOT NULL
                    )
                """)
                
                cur.execute("SELECT COUNT(*) FROM ventes")
                if cur.fetchone()[0] == 0:
                    self._insert_sample_sales(cur)
                
                conn.commit()
    
    def _insert_sample_sales(self, cur):
        """Insert sample sales data (same as fake data)"""
        import uuid
        
        magasins = ["magasin 1", "magasin 2", "magasin 3", "magasin 4", "magasin 5"]
        produits = ["1", "2", "3", "4", "5"]
        prix = {"1": 1.99, "2": 2.49, "3": 4.99, "4": 1.99, "5": 2.79}
        
        # Generate vente pour last 30 days
        for jour in range(30):
            date_vente = datetime.now() - timedelta(days=jour)
            
            for magasin in magasins:
                nb_ventes = 3 + (jour % 6)
                
                for i in range(nb_ventes):
                    produit_id = produits[i % len(produits)]
                    quantite = 1 + (i % 4)
                    prix_unitaire = prix[produit_id]
                    total = quantite * prix_unitaire
                    
                    cur.execute("""
                        INSERT INTO ventes (id, magasin_id, produit_id, quantite, prix_unitaire, total, date_vente)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (
                        str(uuid.uuid4()),
                        magasin,
                        produit_id,
                        quantite,
                        prix_unitaire,
                        total,
                        date_vente
                    ))
    
    def get_ventes_by_magasin(self, magasin_id: str) -> List[Vente]:
        """Get sales for specific store from PostgreSQL"""
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, magasin_id, produit_id, quantite, prix_unitaire, total, date_vente
                    FROM ventes WHERE magasin_id = %s
                    ORDER BY date_vente DESC
                """, (magasin_id,))
                
                ventes = []
                for row in cur.fetchall():
                    ventes.append(Vente(
                        id=row[0],
                        magasin_id=row[1],
                        produit_id=row[2],
                        quantite=row[3],
                        prix_unitaire=float(row[4]),
                        total=float(row[5]),
                        date_vente=row[6]
                    ))
                return ventes
    
    def get_ventes_by_periode(self, date_debut: datetime, date_fin: datetime) -> List[Vente]:
        """Get sales for date range from PostgreSQL"""
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, magasin_id, produit_id, quantite, prix_unitaire, total, date_vente
                    FROM ventes 
                    WHERE date_vente BETWEEN %s AND %s
                    ORDER BY date_vente DESC
                """, (date_debut, date_fin))
                
                ventes = []
                for row in cur.fetchall():
                    ventes.append(Vente(
                        id=row[0],
                        magasin_id=row[1],
                        produit_id=row[2],
                        quantite=row[3],
                        prix_unitaire=float(row[4]),
                        total=float(row[5]),
                        date_vente=row[6]
                    ))
                return ventes
    
    def get_total_ventes_par_magasin(self) -> Dict[str, float]:
        """Get total sales by store from PostgreSQL"""
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT magasin_id, SUM(total)
                    FROM ventes
                    GROUP BY magasin_id
                """)
                
                return dict(cur.fetchall())
    
    def get_produits_plus_vendus(self, limite: int = 10) -> List[tuple]:
        """Get best selling products from PostgreSQL"""
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT produit_id, SUM(quantite) as total_quantite
                    FROM ventes
                    GROUP BY produit_id
                    ORDER BY total_quantite DESC
                    LIMIT %s
                """, (limite,))
                
                return cur.fetchall()
    
    def add_vente(self, vente: Vente) -> bool:
        """Add new sale to PostgreSQL"""
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO ventes (id, magasin_id, produit_id, quantite, prix_unitaire, total, date_vente)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (
                        vente.id,
                        vente.magasin_id,
                        vente.produit_id,
                        vente.quantite,
                        vente.prix_unitaire,
                        vente.total,
                        vente.date_vente
                    ))
                    
                    conn.commit()
                    return True
        except Exception as e:
            print(f"Error adding sale: {e}")
            return False
