"""
Modèle pour UC3 - Tableau de bord performances
"""
from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime


@dataclass
class AlerteStock:
    """Alerte de rupture ou surstock"""
    produit_id: str
    nom_produit: str
    stock_actuel: int
    seuil_critique: int
    type_alerte: str  
    
    def __str__(self):
        return f"{self.type_alerte}: {self.nom_produit} ({self.stock_actuel})"


@dataclass
class PerformanceMagasin:
    """Performance d'un magasin"""
    magasin_id: str
    ventes_totales: float
    nb_transactions: int
    vente_moyenne: float
    performance_relative: str 
    
    def __str__(self):
        return f"{self.magasin_id}: ${self.ventes_totales:.2f} ({self.performance_relative})"

# pourcentage d'évolution vs semaine précédente avec tendance soit "HAUSSE", "BAISSE", "STABLE"
@dataclass
class TendanceHebdomadaire:
    """Tendance des ventes sur 7 jours"""
    semaine: str
    ventes_totales: float
    evolution: float  
    tendance: str 
    
    def __str__(self):
        return f"Semaine {self.semaine}: ${self.ventes_totales:.2f} ({self.tendance})"


@dataclass
class TableauBord:
    """Tableau de bord UC3"""
    date_generation: datetime
    performances_magasins: List[PerformanceMagasin]
    alertes_stock: List[AlerteStock]
    tendances_hebdomadaires: List[TendanceHebdomadaire]
    total_reseau: float
    
    def __str__(self):
        return f"Dashboard {self.date_generation.strftime('%Y-%m-%d')}: {len(self.performances_magasins)} magasins, {len(self.alertes_stock)} alertes"
