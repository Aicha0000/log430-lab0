"""
Module qui initialise la base de donnees SQLite pour ouvrir une session
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base

#Connexion a la base de donnees SQLite - en mémoire pour les tests
engine = create_engine("sqlite:///:memory:", echo=True)

#Creation de la base de donnees dans app.models
Base.metadata.create_all(engine)

#Session pour interagir avec la base de donnees
Session = sessionmaker(bind=engine)
session = Session()