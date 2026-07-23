from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from app.database import engine, get_db, Base
from app.db_models import DBProducto, DBMovimientoKardex
from app.models import Producto
from app.schemas import ProductoCreate, MovimientoCreate
from app.analytics import InventarioAnalytics

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema Profesional de Inventarios", version="4.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def sembrar_datos_iniciales():
    db = next(get_db())
    if db.query(DBProducto).count() == 0:
        p1 = DBProducto(nombre="Laptop Lenovo LOQ", marca="Lenovo", categoria="Tecnología", precio_costo=2800.00, precio_venta=3200.00, stock=0, min_stock=3, max_stock=15, imagen="https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=500&q=80")
        p2 = DBProducto(nombre="Mouse Gamer RGB", marca="Logitech", categoria="Tecnología", precio_costo=80.00, precio_venta=120.00, stock=0, min_stock=5, max_stock=20, imagen="https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=500&q=80")
        
        db.add_all([p1, p2])
        db.commit()

        for p, cant in [(p1, 10), (p2, 2)]:
            p.stock += cant
            db.add(DBMovimientoKardex(
                producto_id=p.id,
                producto_nombre=p.nombre,
                tipo="ENTRADA",
                cantidad=cant,
                motivo="Compra inicial a proveedor",
                usuario="Administrador"
            ))
        db.commit()

sembrar_datos_iniciales()

def db_to_poo(p_db: DBProducto) -> Producto:
    return Producto(
        id_prod=p_db.id,
        nombre=p_db.nombre,
        marca=p_db.marca or "Genérica",
        categoria=p_db.categoria,
        precio_costo=p_db.precio_costo,
        precio_venta=p_db.precio_venta,
        stock=p_db.stock,
        min_stock=p_db.min_stock,
        max_stock=p_db.max_stock or 50,
        imagen=p_db.imagen
    )



@app.get("/api/productos")
def listar_productos(db: Session = Depends(get_db)):
    productos_db = db.query(DBProducto).all()
    return [db_to_poo(p).to_dict() for p in productos_db]

@app.post("/api/productos", status_code=status.HTTP_201_CREATED)
def crear_producto(datos: ProductoCreate, db: Session = Depends(get_db)):
    nuevo_p = DBProducto(
        nombre=datos.nombre,
        marca=datos.marca,
        categoria=datos.categoria,
        precio_costo=datos.precio_costo,
        precio_venta=datos.precio_venta,
        stock=0,
        min_stock=datos.min_stock,
        max_stock=datos.max_stock,
        imagen=datos.imagen or ""
    )
    db.add(nuevo_p)
    db.commit()
    db.refresh(nuevo_p)

    return db_to_poo(nuevo_p).to_dict()

@app.put("/api/productos/{id_prod}")
def actualizar_producto(id_prod: int, datos: ProductoCreate, db: Session = Depends(get_db)):
    prod_db = db.query(DBProducto).filter(DBProducto.id == id_prod).first()
    if not prod_db:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    prod_db.nombre = datos.nombre
    prod_db.marca = datos.marca
    prod_db.categoria = datos.categoria
    prod_db.precio_costo = datos.precio_costo
    prod_db.precio_venta = datos.precio_venta
    prod_db.min_stock = datos.min_stock
    prod_db.max_stock = datos.max_stock
    if datos.imagen:
        prod_db.imagen = datos.imagen

    db.commit()
    return {"mensaje": "Producto actualizado", "producto": db_to_poo(prod_db).to_dict()}

@app.delete("/api/productos/{id_prod}")
def eliminar_producto(id_prod: int, db: Session = Depends(get_db)):
    prod_db = db.query(DBProducto).filter(DBProducto.id == id_prod).first()
    if not prod_db:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    db.delete(prod_db)
    db.commit()
    return {"mensaje": "Producto eliminado"}

@app.post("/api/productos/{id_prod}/movimiento")
def registrar_movimiento(id_prod: int, mov: MovimientoCreate, db: Session = Depends(get_db)):
    prod_db = db.query(DBProducto).filter(DBProducto.id == id_prod).first()
    if not prod_db:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    prod_poo = db_to_poo(prod_db)
    try:
        prod_poo.actualizar_stock_desde_kardex(mov.cantidad)
        prod_db.stock = prod_poo.stock

        tipo_mov = "ENTRADA" if mov.cantidad > 0 else "SALIDA"
        db.add(DBMovimientoKardex(
            producto_id=prod_db.id,
            producto_nombre=prod_db.nombre,
            tipo=tipo_mov,
            cantidad=abs(mov.cantidad),
            motivo=mov.motivo,
            usuario=mov.usuario or "Administrador"
        ))
        
        db.commit()
        return {"mensaje": "Stock actualizado desde Kárdex", "producto": prod_poo.to_dict()}
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))

@app.get("/api/kardex")
def obtener_kardex(db: Session = Depends(get_db)):
    kardex_db = db.query(DBMovimientoKardex).order_by(DBMovimientoKardex.id.desc()).all()
    return [
        {
            "id": k.id,
            "producto_id": k.producto_id,
            "producto_nombre": k.producto_nombre,
            "tipo": k.tipo,
            "cantidad": k.cantidad,
            "motivo": k.motivo,
            "usuario": k.usuario,
            "fecha": k.fecha
        }
        for k in kardex_db
    ]

@app.get("/api/analytics/dashboard")
def obtener_metricas_dashboard(db: Session = Depends(get_db)):
    productos_db = db.query(DBProducto).all()
    productos_poo = [db_to_poo(p) for p in productos_db]

    return {
        "valor_inversion": InventarioAnalytics.calcular_valor_total_inversion(productos_poo),
        "valor_venta": InventarioAnalytics.calcular_valor_total_venta(productos_poo),
        "alertas_stock": InventarioAnalytics.obtener_alertas_reabastecimiento(productos_poo),
        "valor_por_categoria": InventarioAnalytics.agrupar_valor_por_categoria(productos_poo),
        "estadisticas_numpy": InventarioAnalytics.calcular_estadisticas_numpy(productos_poo)
    }