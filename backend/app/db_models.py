from sqlalchemy import Column, Integer, String, Float
from datetime import datetime
from app.database import Base

class DBProducto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    marca = Column(String)
    categoria = Column(String)
    precio_costo = Column(Float) # Precio de compra (para valoración e inversión real)
    precio_venta = Column(Float) # Precio al público (para margen de ganancia)
    stock = Column(Integer, default=0) # SALDO: Solo modificable por Kardex
    min_stock = Column(Integer)  # Punto de reorden (Stock Mínimo)
    max_stock = Column(Integer)  # Capacidad máxima recomendada
    imagen = Column(String)

class DBMovimientoKardex(Base):
    __tablename__ = "kardex"

    id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer)
    producto_nombre = Column(String)
    tipo = Column(String)        # "ENTRADA" o "SALIDA"
    cantidad = Column(Integer)
    motivo = Column(String)      # "Compra", "Venta", "Merma", "Ajuste"
    usuario = Column(String, default="Administrador") # Para el Pilar 5 (Seguridad)
    fecha = Column(String, default=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))