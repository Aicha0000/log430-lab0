
import psycopg2
from typing import List, Optional
import os
from datetime import datetime

from commun.repositories.stock_repository import StockRepository
from commun.modeles.produit import Produit, DemandeReapprovisionnement


class PostgreSQLStockRepository(StockRepository):

    
    def __init__(self):
        self.connection_string = os.getenv(
            "DATABASE_URL", 
            "postgresql://user:password@localhost:5432/lab2_db"
        )
        self._demande_counter = 0
        self._demandes = []
        self._init_tables()
    
    def _get_connection(self):

        return psycopg2.connect(self.connection_string)
    
    def _init_tables(self):

        with self._get_connection() as conn:
            with conn.cursor() as cur:

                cur.execute("""
                    CREATE TABLE IF NOT EXISTS produits (
                        id VARCHAR PRIMARY KEY,
                        nom VARCHAR NOT NULL,
                        description TEXT,
                        prix DECIMAL(10,2) NOT NULL,
                        stock_central INTEGER NOT NULL,
                        seuil_critique INTEGER NOT NULL DEFAULT 10
                    )
                """)
                
  
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS demandes_reapprovisionnement (
                        id VARCHAR PRIMARY KEY,
                        magasin_id VARCHAR NOT NULL,
                        produit_id VARCHAR NOT NULL,
                        quantite_demandee INTEGER NOT NULL,
                        statut VARCHAR NOT NULL DEFAULT 'EN_ATTENTE',
                        created_at TIMESTAMP NOT NULL,
                        FOREIGN KEY (produit_id) REFERENCES produits(id)
                    )
                """)
                

                cur.execute("SELECT COUNT(*) FROM produits")
                if cur.fetchone()[0] == 0:
                    self._insert_initial_data(cur)
                
                conn.commit()
    
    def _insert_initial_data(self, cur):

        products = [
            ("1", "Coca-Cola", "Boisson gazeuse classique", 1.99, 150, 10),
            ("2", "Snapple", "Jus de pomme naturel", 2.49, 8, 10),
            ("3", "Jus Orange Tropicana", "Jus orange naturel", 4.99, 45, 10),
            ("4", "Sprite", "Boisson gazeuse citron-lime", 1.99, 120, 10),
            ("5", "Frutopia", "Boisson aux fruits", 2.79, 5, 10)
        ]
        
        for product in products:
            cur.execute("""
                INSERT INTO produits (id, nom, description, prix, stock_central, seuil_critique)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, product)
    
    def get_produit_by_id(self, produit_id: str) -> Optional[Produit]:

        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, nom, description, prix, stock_central, seuil_critique
                    FROM produits WHERE id = %s
                """, (produit_id,))
                
                row = cur.fetchone()
                if row:
                    return Produit(
                        id=row[0],
                        nom=row[1], 
                        description=row[2],
                        prix=float(row[3]),
                        stock_central=row[4],
                        seuil_critique=row[5]
                    )
                return None
    
    def get_all_produits(self) -> List[Produit]:

        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, nom, description, prix, stock_central, seuil_critique
                    FROM produits ORDER BY nom
                """)
                
                products = []
                for row in cur.fetchall():
                    products.append(Produit(
                        id=row[0],
                        nom=row[1],
                        description=row[2], 
                        prix=float(row[3]),
                        stock_central=row[4],
                        seuil_critique=row[5]
                    ))
                return products
    
    def search_produits(self, terme: str) -> List[Produit]:

        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, nom, description, prix, stock_central, seuil_critique
                    FROM produits 
                    WHERE LOWER(nom) LIKE %s OR LOWER(description) LIKE %s
                    ORDER BY nom
                """, (f"%{terme.lower()}%", f"%{terme.lower()}%"))
                
                products = []
                for row in cur.fetchall():
                    products.append(Produit(
                        id=row[0],
                        nom=row[1],
                        description=row[2],
                        prix=float(row[3]),
                        stock_central=row[4],
                        seuil_critique=row[5]
                    ))
                return products
    
    def create_demande_reapprovisionnement(self, demande: DemandeReapprovisionnement) -> bool:

        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    # Generate ID if not provided
                    if not demande.id:
                        cur.execute("SELECT COUNT(*) FROM demandes_reapprovisionnement")
                        count = cur.fetchone()[0]
                        demande.id = f"no{count + 1}"
                    
                    cur.execute("""
                        INSERT INTO demandes_reapprovisionnement 
                        (id, magasin_id, produit_id, quantite_demandee, statut, created_at)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (
                        demande.id,
                        demande.magasin_id,
                        demande.produit_id,
                        demande.quantite_demandee,
                        demande.statut,
                        demande.created_at or datetime.now()
                    ))
                    
                    conn.commit()
                    return True
        except Exception as e:
            print(f"Error creating replenishment request: {e}")
            return False
    
    def get_demandes_reapprovisionnement(self) -> List[DemandeReapprovisionnement]:
        # For testing: use in-memory list if it has items
        if hasattr(self, '_demandes') and self._demandes:
            return self._demandes
        
        # Otherwise use database
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, magasin_id, produit_id, quantite_demandee, statut, created_at
                    FROM demandes_reapprovisionnement
                    ORDER BY created_at DESC
                """)
                
                demandes = []
                for row in cur.fetchall():
                    demandes.append(DemandeReapprovisionnement(
                        id=row[0],
                        magasin_id=row[1],
                        produit_id=row[2],
                        quantite_demandee=row[3],
                        statut=row[4],
                        created_at=row[5]
                    ))
                return demandes
    
    def update_demande_statut(self, demande_id: str, status: str) -> bool:
        # For testing: update in-memory list if it exists
        if hasattr(self, '_demandes') and self._demandes:
            for demande in self._demandes:
                if demande.id == demande_id:
                    demande.statut = status
                    return True
            return False
        
        # Otherwise update database
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        UPDATE demandes_reapprovisionnement 
                        SET statut = %s 
                        WHERE id = %s
                    """, (status, demande_id))
                    
                    conn.commit()
                    return cur.rowcount > 0
        except Exception as e:
            print(f"Error updating request status: {e}")
            return False
    
    def update_stock(self, produit_id: str, qty: int) -> bool:

        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        UPDATE produits SET stock_central = %s WHERE id = %s
                    """, (qty, produit_id))
                    
                    conn.commit()
                    return cur.rowcount > 0
        except Exception as e:
            print(f"Error updating stock: {e}")
            return False
    
    def update_product(self, produit_id: str, nom: str = None, prix: float = None, description: str = None) -> bool:

        try:
            updates = []
            params = []
            
            if nom is not None:
                updates.append("nom = %s")
                params.append(nom)
            
            if prix is not None:
                updates.append("prix = %s")
                params.append(prix)
            
            if description is not None:
                updates.append("description = %s")
                params.append(description)
            
            if not updates:
                return False
            
            params.append(produit_id)
            
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    query = f"UPDATE produits SET {', '.join(updates)} WHERE id = %s"
                    cur.execute(query,params)
                    
                    conn.commit()
                    return cur.rowcount > 0
        except Exception as e:
            print(f"Error updating product: {e}")
            return False
