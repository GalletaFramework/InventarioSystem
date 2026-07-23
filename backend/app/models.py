from datetime import datetime

# --- POO: Clase Padre ---
class ItemInventario:
    def __init__(self, id_item: int, nombre: str, precio_costo: float, precio_venta: float):
        self._id = id_item
        self.nombre = nombre
        self.precio_costo = precio_costo
        self.precio_venta = precio_venta

    @property
    def id(self) -> int:
        return self._id

    def obtener_sku(self) -> str:
        """Uso de split() para generar código SKU dinámico a partir de las iniciales."""
        palabras = self.nombre.split(" ")
        iniciales = "".join([p[0].upper() for p in palabras if p])
        return f"SKU-{iniciales}-{self._id:03d}"

    def calcular_margen_ganancia(self) -> float:
        """Calcula la ganancia bruta unitaria."""
        return round(self.precio_venta - self.precio_costo, 2)


# --- POO: Clase Hija ---
class Producto(ItemInventario):
    def __init__(self, id_prod: int, nombre: str, marca: str, categoria: str, 
                 precio_costo: float, precio_venta: float, stock: int, 
                 min_stock: int, max_stock: int, imagen: str = ""):
        super().__init__(id_item=id_prod, nombre=nombre, precio_costo=precio_costo, precio_venta=precio_venta)
        self.marca = marca
        self.categoria = categoria
        self._stock = stock
        self.min_stock = min_stock
        self.max_stock = max_stock
        self.imagen = imagen if imagen else "https://images.unsplash.com/photo-1526738549149-8e07eca6c147?w=500&q=80"

    @property
    def stock(self) -> int:
        return self._stock

    def actualizar_stock_desde_kardex(self, cantidad: int) -> None:
        """Regla de Negocio: El stock SOLO cambia a través de movimientos de Kardex."""
        if self._stock + cantidad < 0:
            raise ValueError(f"Stock insuficiente para '{self.nombre}'. Saldo actual: {self._stock} u., Intento de retiro: {abs(cantidad)} u.")
        self._stock += cantidad

    def obtener_estado_semaforo(self) -> dict:
        """PILAR 3: Semaforización visual de reabastecimiento."""
        if self._stock == 0:
            return {"estado": "CRÍTICO / AGOTADO", "color": "🔴", "codigo": "rojo"}
        elif self._stock <= self.min_stock:
            return {"estado": "POR AGOTARSE", "color": "🟡", "codigo": "amarillo"}
        else:
            return {"estado": "NORMAL", "color": "🟢", "codigo": "verde"}

    def to_dict(self) -> dict:
        semaforo = self.obtener_estado_semaforo()
        return {
            "id": self._id,
            "sku": self.obtener_sku(),
            "nombre": self.nombre,
            "marca": self.marca,
            "categoria": self.categoria,
            "precio_costo": self.precio_costo,
            "precio_venta": self.precio_venta,
            "margen_ganancia": self.calcular_margen_ganancia(),
            "stock": self._stock,
            "min_stock": self.min_stock,
            "max_stock": self.max_stock,
            "imagen": self.imagen,
            "estado_stock": semaforo["estado"],
            "color_semaforo": semaforo["color"],
            "alerta": semaforo["codigo"] != "verde"
        }