import numpy as np
from functools import reduce
from typing import List
from app.models import Producto

class InventarioAnalytics:

    @staticmethod
    def calcular_valor_total_inversion(productos: List[Producto]) -> float:
        if not productos:
            return 0.0
        costos_totales = map(lambda p: p.precio_costo * p.stock, productos)
        return round(reduce(lambda acc, val: acc + val, costos_totales, 0.0), 2)

    @staticmethod
    def calcular_valor_total_venta(productos: List[Producto]) -> float:
        if not productos:
            return 0.0
        ventas_totales = map(lambda p: p.precio_venta * p.stock, productos)
        return round(reduce(lambda acc, val: acc + val, ventas_totales, 0.0), 2)

    @staticmethod
    def obtener_alertas_reabastecimiento(productos: List[Producto]) -> List[dict]:
        """Filtra los productos que alcanzaron el stock mínimo."""
        criticos = filter(lambda p: p.stock <= p.min_stock, productos)
        return list(map(lambda p: p.to_dict(), criticos))

    @staticmethod
    def agrupar_valor_por_categoria(productos: List[Producto]) -> dict:
        """Agrupa el valor en costo por categoría."""
        categorias = set(map(lambda p: p.categoria, productos))
        return {
            cat: round(
                sum(map(lambda p: p.precio_costo * p.stock, filter(lambda p: p.categoria == cat, productos))),
                2
            )
            for cat in categorias
        }

    @staticmethod
    def calcular_estadisticas_numpy(productos: List[Producto]) -> dict:
        if not productos:
            return {"costo_promedio": 0.0, "ganancia_promedio": 0.0, "stock_total": 0}

        costos = np.array([p.precio_costo for p in productos])
        ventas = np.array([p.precio_venta for p in productos])
        margenes = ventas - costos
        stocks = np.array([p.stock for p in productos])

        return {
            "costo_promedio": round(float(np.mean(costos)), 2),
            "precio_venta_promedio": round(float(np.mean(ventas)), 2),
            "margen_ganancia_promedio": round(float(np.mean(margenes)), 2),
            "desviacion_precios": round(float(np.std(ventas)), 2),
            "stock_total_unidades": int(np.sum(stocks))
        }