from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Crea un archivo 'inventario.db' localmente en la carpeta del backend
SQLALCHEMY_DATABASE_URL = "sqlite:///./inventario.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Helper para obtener la sesión de base de datos por petición
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()