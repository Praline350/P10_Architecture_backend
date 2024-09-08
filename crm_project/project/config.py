from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuration de la connexion à la base de données
DATABASE_URL = "mysql+mysqldb://admin:ChillAdmin3500!@localhost:3306/epic_event"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour les modèles SQLAlchemy
Base = declarative_base()


#color back #88A0A8 #546A76

