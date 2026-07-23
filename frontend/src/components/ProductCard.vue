<template>
  <div class="bg-white rounded-2xl p-4 border border-slate-100 shadow-sm hover:shadow-md transition relative group">
    
    <div class="absolute top-4 right-4 z-10">
      <button @click="menuAbierto = !menuAbierto" class="text-slate-400 hover:text-slate-600 p-1 rounded-lg hover:bg-slate-100 cursor-pointer">
        <MoreVertical class="w-4 h-4" />
      </button>

      <div v-if="menuAbierto" class="absolute right-0 mt-1 w-32 bg-white rounded-xl shadow-lg border border-slate-100 py-1 z-20">
        <button @click="abrirEdicion" class="w-full text-left px-3 py-1.5 text-xs font-medium text-slate-700 hover:bg-slate-50 flex items-center gap-2 cursor-pointer">
          ✏️ Editar
        </button>
        <button @click="confirmarEliminar" class="w-full text-left px-3 py-1.5 text-xs font-medium text-rose-600 hover:bg-rose-50 flex items-center gap-2 cursor-pointer">
          🗑️ Eliminar
        </button>
      </div>
    </div>

    <!-- Imagen -->
    <div class="h-36 w-full flex items-center justify-center bg-slate-50 rounded-xl mb-3 p-2 overflow-hidden">
      <img :src="producto.imagen" :alt="producto.nombre" @error="imagenError" class="h-full w-full object-contain hover:scale-105 transition-transform duration-300" />
    </div>

    <!-- Título y SKU -->
    <div class="flex items-center justify-between mb-1">
      <span class="text-[10px] font-mono font-bold bg-slate-100 text-slate-600 px-2 py-0.5 rounded-md">
        {{ producto.sku }}
      </span>
      <span class="text-xs font-bold" title="Estado de Stock">
        {{ producto.color_semaforo }} {{ producto.estado_stock }}
      </span>
    </div>

    <h3 class="font-bold text-slate-800 text-sm mb-1 line-clamp-1">{{ producto.nombre }}</h3>
    <p class="text-xs text-slate-400 mb-2">{{ producto.marca }} • <span class="text-slate-600 font-medium">{{ producto.categoria }}</span></p>

    <!-- Precios y Margen -->
    <div class="flex items-baseline justify-between mb-3 bg-slate-50 p-2 rounded-xl border border-slate-100">
      <div>
        <span class="text-[10px] text-slate-400 block uppercase font-semibold">Precio Venta</span>
        <span class="text-base font-extrabold text-slate-900">S/. {{ producto.precio_venta.toFixed(2) }}</span>
      </div>
      <div class="text-right">
        <span class="text-[10px] text-slate-400 block uppercase font-semibold">Margen Unit.</span>
        <span class="text-xs font-bold text-emerald-600">+S/. {{ producto.margen_ganancia.toFixed(2) }}</span>
      </div>
    </div>

    <!-- Pie de Tarjeta: Stock Físico (Solo modificable por Kárdex) -->
    <div class="pt-2 border-t border-slate-100 flex items-center justify-between">
      <span class="text-xs font-semibold text-slate-500">
        Stock: <strong class="text-slate-900 text-sm">{{ producto.stock }}</strong> / {{ producto.max_stock }} u.
      </span>
      
      <div class="flex gap-1">
        <button @click="$emit('modificar-stock', producto.id, 1)" class="px-2.5 py-1 bg-emerald-50 hover:bg-emerald-100 text-emerald-700 rounded-lg text-xs font-bold transition cursor-pointer" title="Registrar Entrada Kárdex">
          +1 Ent
        </button>
        <button @click="$emit('modificar-stock', producto.id, -1)" class="px-2.5 py-1 bg-rose-50 hover:bg-rose-100 text-rose-700 rounded-lg text-xs font-bold transition cursor-pointer" title="Registrar Salida Kárdex">
          -1 Sal
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { MoreVertical } from 'lucide-vue-next'

const props = defineProps({
  producto: Object
})

const emit = defineEmits(['modificar-stock', 'editar-producto', 'eliminar-producto'])

const menuAbierto = ref(false)

const abrirEdicion = () => {
  menuAbierto.value = false
  emit('editar-producto', props.producto)
}

const confirmarEliminar = () => {
  menuAbierto.value = false
  if (confirm(`¿Eliminar definitivamente "${props.producto.nombre}"?`)) {
    emit('eliminar-producto', props.producto.id)
  }
}

const imagenError = (event) => {
  event.target.src = 'https://images.unsplash.com/photo-1526738549149-8e07eca6c147?w=500&q=80'
}
</script>