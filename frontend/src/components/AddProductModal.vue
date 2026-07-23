<template>
  <div v-if="isOpen" class="fixed inset-0 bg-slate-900/50 backdrop-blur-sm flex items-center justify-center p-4 z-50">
    <div class="bg-white rounded-2xl max-w-md w-full p-6 shadow-xl border border-slate-100 animate-fade-in">
      
      <div class="flex justify-between items-center mb-5 border-b border-slate-100 pb-3">
        <h3 class="font-bold text-slate-800 text-lg">
          {{ productoEdit ? 'Editar Producto' : 'Añadir Nuevo Producto' }}
        </h3>
        <button @click="$emit('close')" class="text-slate-400 hover:text-slate-600 font-bold p-1 rounded-lg transition">
          ✕
        </button>
      </div>

      <form @submit.prevent="guardar" class="space-y-3">
        <div>
          <label class="block text-xs font-semibold text-slate-500 mb-1">Nombre del Producto</label>
          <input v-model="form.nombre" required type="text" placeholder="Ej. Laptop Lenovo LOQ" class="w-full bg-slate-50 border border-slate-200 rounded-xl p-2.5 text-xs text-slate-800 focus:outline-none" />
        </div>

        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block text-xs font-semibold text-slate-500 mb-1">Marca</label>
            <input v-model="form.marca" required type="text" placeholder="Lenovo" class="w-full bg-slate-50 border border-slate-200 rounded-xl p-2.5 text-xs text-slate-800 focus:outline-none" />
          </div>
          <div>
            <label class="block text-xs font-semibold text-slate-500 mb-1">Categoría</label>
            <input v-model="form.categoria" required type="text" placeholder="Tecnología" class="w-full bg-slate-50 border border-slate-200 rounded-xl p-2.5 text-xs text-slate-800 focus:outline-none" />
          </div>
        </div>

        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block text-xs font-semibold text-slate-500 mb-1">Precio Costo (S/.)</label>
            <input v-model.number="form.precio_costo" required min="0.1" step="0.01" type="number" placeholder="2800.00" class="w-full bg-slate-50 border border-slate-200 rounded-xl p-2.5 text-xs text-slate-800 focus:outline-none" />
          </div>
          <div>
            <label class="block text-xs font-semibold text-slate-500 mb-1">Precio Venta (S/.)</label>
            <input v-model.number="form.precio_venta" required min="0.1" step="0.01" type="number" placeholder="3200.00" class="w-full bg-slate-50 border border-slate-200 rounded-xl p-2.5 text-xs text-slate-800 focus:outline-none" />
          </div>
        </div>

        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block text-xs font-semibold text-slate-500 mb-1">Stock Mínimo (Alerta)</label>
            <input v-model.number="form.min_stock" required min="1" type="number" placeholder="3" class="w-full bg-slate-50 border border-slate-200 rounded-xl p-2.5 text-xs text-slate-800 focus:outline-none" />
          </div>
          <div>
            <label class="block text-xs font-semibold text-slate-500 mb-1">Stock Máximo</label>
            <input v-model.number="form.max_stock" required min="1" type="number" placeholder="15" class="w-full bg-slate-50 border border-slate-200 rounded-xl p-2.5 text-xs text-slate-800 focus:outline-none" />
          </div>
        </div>

        <div>
          <label class="block text-xs font-semibold text-slate-500 mb-1">Imagen del Producto (Subir desde equipo)</label>
          <input type="file" accept="image/*" @change="procesarImagenLocal" class="w-full text-xs text-slate-500 file:mr-3 file:py-2 file:px-3 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-slate-900 file:text-white cursor-pointer" />
          
          <div v-if="vistaPrevia" class="mt-2 flex items-center gap-3 bg-slate-50 p-2 rounded-xl border border-slate-200">
            <img :src="vistaPrevia" class="h-10 w-10 object-contain rounded-lg bg-white border" />
            <span class="text-[11px] text-slate-500 font-medium">Imagen seleccionada</span>
          </div>
        </div>

        <div class="flex gap-3 pt-3">
          <button type="button" @click="$emit('close')" class="w-1/2 bg-slate-100 hover:bg-slate-200 text-slate-600 font-medium py-2.5 rounded-xl text-xs transition cursor-pointer">
            Cancelar
          </button>
          <button type="submit" class="w-1/2 bg-slate-900 hover:bg-slate-800 text-white font-medium py-2.5 rounded-xl text-xs transition cursor-pointer">
            Guardar Producto
          </button>
        </div>
      </form>

    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  isOpen: Boolean,
  productoEdit: Object
})

const emit = defineEmits(['close', 'crear'])

const form = ref({
  nombre: '',
  marca: '',
  categoria: '',
  precio_costo: null,
  precio_venta: null,
  min_stock: 3,
  max_stock: 20,
  imagen: ''
})

const vistaPrevia = ref('')

watch(() => props.productoEdit, (nuevoVal) => {
  if (nuevoVal) {
    form.value = { ...nuevoVal }
    vistaPrevia.value = nuevoVal.imagen || ''
  } else {
    form.value = { nombre: '', marca: '', categoria: '', precio_costo: null, precio_venta: null, min_stock: 3, max_stock: 20, imagen: '' }
    vistaPrevia.value = ''
  }
}, { immediate: true })

const procesarImagenLocal = (event) => {
  const file = event.target.files[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = (e) => {
      form.value.imagen = e.target.result
      vistaPrevia.value = e.target.result
    }
    reader.readAsDataURL(file)
  }
}

const guardar = () => {
  emit('crear', { ...form.value })
  form.value = { nombre: '', marca: '', categoria: '', precio_costo: null, precio_venta: null, min_stock: 3, max_stock: 20, imagen: '' }
  vistaPrevia.value = ''
}
</script>