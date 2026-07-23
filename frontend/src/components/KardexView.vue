<template>
  <div class="space-y-6 animate-fade-in">
    <div>
      <h1 class="text-2xl font-bold text-slate-900">Historial de Movimientos (Kárdex)</h1>
      <p class="text-xs text-slate-400 mt-1">Trazabilidad en tiempo real de entradas y salidas de almacén</p>
    </div>

    <div class="bg-white rounded-2xl border border-slate-100 p-6 shadow-sm">
      <div class="overflow-x-auto">
        <table class="w-full text-left text-xs text-slate-600">
          <thead class="bg-slate-50 text-slate-400 uppercase font-semibold border-b border-slate-100">
            <tr>
              <th class="p-3">ID</th>
              <th class="p-3">Fecha y Hora</th>
              <th class="p-3">Producto</th>
              <th class="p-3">Tipo</th>
              <th class="p-3">Cantidad</th>
              <th class="p-3">Motivo / Justificación</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100">
            <tr v-for="item in kardex" :key="item.id" class="hover:bg-slate-50/50">
              <td class="p-3 font-mono font-bold text-slate-400">#{{ item.id }}</td>
              <td class="p-3 text-slate-500">{{ item.fecha }}</td>
              <td class="p-3 font-semibold text-slate-800">{{ item.producto_nombre }}</td>
              <td class="p-3">
                <span 
                  :class="item.tipo === 'ENTRADA' ? 'bg-emerald-50 text-emerald-600 border-emerald-200' : 'bg-rose-50 text-rose-600 border-rose-200'" 
                  class="px-2.5 py-1 rounded-lg text-[10px] font-bold border"
                >
                  {{ item.tipo }}
                </span>
              </td>
              <td class="p-3 font-bold text-slate-900">
                {{ item.tipo === 'ENTRADA' ? '+' : '-' }}{{ item.cantidad }}
              </td>
              <td class="p-3 text-slate-500 italic">{{ item.motivo }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  kardex: Array
})
</script>