from sqlalchemy import Column, Integer, String, Float
from datetime import datetime
from app.database import Base

class DBProducto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    marca = Column(String)
    categoria = Column(String)
    precio_costo = Column(Float)
    precio_venta = Column(Float)
    stock = Column(Integer, default=0) 
    min_stock = Column(Integer)  
    max_stock = Column(Integer)  
    imagen = Column(String)

class DBMovimientoKardex(Base):
    __tablename__ = "kardex"

    id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer)
    producto_nombre = Column(String)
    tipo = Column(String)     
    cantidad = Column(Integer)
    motivo = Column(String)     
    usuario = Column(String, default="Administrador") # Para el Pilar 5 (Seguridad)
    fecha = Column(String, default=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))