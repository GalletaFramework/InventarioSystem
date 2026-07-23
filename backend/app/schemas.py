from pydantic import BaseModel, Field
from typing import Optional

class ProductoCreate(BaseModel):
    nombre: str
    marca: str
    categoria: str
    precio_costo: float = Field(gt=0, description="Precio de compra")
    precio_venta: float = Field(gt=0, description="Precio de venta al público")
    min_stock: int = Field(ge=1, description="Stock Mínimo / Punto de Reorden")
    max_stock: int = Field(ge=1, description="Stock Máximo de capacidad")
    imagen: Optional[str] = ""

class MovimientoCreate(BaseModel):
    cantidad: int # Positivo para Entrada (Compra), Negativo para Salida (Venta/Merma)
    motivo: str = Field(description="Ej. Compra a proveedor, Venta, Merma, Devolución")
    usuario: Optional[str] = "Administrador"