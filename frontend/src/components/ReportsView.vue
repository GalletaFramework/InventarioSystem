<template>
  <div class="space-y-8 animate-fade-in">
    <div>
      <h1 class="text-2xl font-bold text-slate-900">Reportes Financieros y Analytics</h1>
    </div>

    <!-- TARJETAS PRINCIPALES DE VALORACIÓN -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm">
        <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Inversión Retenida (Costo)</span>
        <p class="text-3xl font-extrabold text-slate-900 mt-2">S/. {{ dashboard.valor_inversion || 0 }}</p>
        <p class="text-xs text-slate-400 mt-2">Capital en mercadería activa</p>
      </div>

      <div class="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm">
        <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Valor Proyectado de Venta</span>
        <p class="text-3xl font-extrabold text-emerald-600 mt-2">S/. {{ dashboard.valor_venta || 0 }}</p>
        <p class="text-xs text-emerald-600 mt-2 font-medium">Ganancia Est.: S/. {{ ((dashboard.valor_venta || 0) - (dashboard.valor_inversion || 0)).toFixed(2) }}</p>
      </div>

      <div class="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm">
        <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Stock Crítico / Alertas</span>
        <p class="text-3xl font-extrabold text-rose-500 mt-2">
          {{ dashboard.alertas_stock ? dashboard.alertas_stock.length : 0 }} Productos
        </p>
        <p class="text-xs text-rose-400 mt-2 font-medium">Punto de reorden alcanzado</p>
      </div>
    </div>

    <!-- CÁLCULOS  CON NUMPY -->
    <div class="bg-slate-900 text-white p-6 rounded-2xl shadow-md border border-slate-800">
      <h3 class="text-sm font-bold text-indigo-400 uppercase tracking-wider mb-4 flex items-center gap-2">
        REPORTE DETALLADO
      </h3>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
        <div class="bg-slate-800/60 p-4 rounded-xl border border-slate-700">
          <span class="text-xs text-slate-400">Costo Promedio Unitario</span>
          <p class="text-xl font-bold text-white mt-1">S/. {{ dashboard.estadisticas_numpy?.costo_promedio || 0 }}</p>
        </div>
        <div class="bg-slate-800/60 p-4 rounded-xl border border-slate-700">
          <span class="text-xs text-slate-400">Margen Promedio Unit.</span>
          <p class="text-xl font-bold text-emerald-400 mt-1">+S/. {{ dashboard.estadisticas_numpy?.margen_ganancia_promedio || 0 }}</p>
        </div>
        <div class="bg-slate-800/60 p-4 rounded-xl border border-slate-700">
          <span class="text-xs text-slate-400">Desviación Estándar</span>
          <p class="text-xl font-bold text-indigo-300 mt-1">± {{ dashboard.estadisticas_numpy?.desviacion_precios || 0 }}</p>
        </div>
        <div class="bg-slate-800/60 p-4 rounded-xl border border-slate-700">
          <span class="text-xs text-slate-400">Stock Físico Total</span>
          <p class="text-xl font-bold text-amber-400 mt-1">{{ dashboard.estadisticas_numpy?.stock_total_unidades || 0 }} u.</p>
        </div>
      </div>
    </div>

    <!-- TABLA POR CATEGORÍA Y ALERTAS -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <div class="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm">
        <h3 class="font-bold text-slate-800 mb-4">Capital Invertido por Categoría</h3>
        <div class="space-y-4">
          <div v-for="(valor, cat) in dashboard.valor_por_categoria" :key="cat" class="flex justify-between items-center pb-3 border-b border-slate-100">
            <span class="text-sm font-medium text-slate-600">{{ cat }}</span>
            <span class="text-sm font-bold text-slate-900">S/. {{ valor.toFixed(2) }}</span>
          </div>
        </div>
      </div>

      <div class="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm">
        <h3 class="font-bold text-slate-800 mb-4 text-rose-600 flex items-center gap-2">
          Reabastecimiento Requerido
        </h3>
        <div v-if="dashboard.alertas_stock && dashboard.alertas_stock.length > 0" class="space-y-3">
          <div v-for="item in dashboard.alertas_stock" :key="item.id" class="flex justify-between items-center p-3 bg-rose-50/50 rounded-xl border border-rose-100">
            <div>
              <p class="text-sm font-bold text-slate-800">{{ item.nombre }}</p>
              <p class="text-xs text-slate-400">{{ item.sku }} | Mín: {{ item.min_stock }} u.</p>
            </div>
            <span class="text-xs font-bold text-rose-600 bg-white px-3 py-1 rounded-lg border border-rose-200">
              Stock: {{ item.stock }}
            </span>
          </div>
        </div>
        <div v-else class="text-xs text-slate-400 italic">
          No hay productos con stock por debajo del límite mínimo.
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  dashboard: Object
})
</script>