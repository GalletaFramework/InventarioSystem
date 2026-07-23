<template>
  <div class="flex min-h-screen bg-slate-100/70 font-sans">
    
    <!-- BARRA LATERAL -->
    <aside class="w-64 bg-slate-50 border-r border-slate-200 p-6 flex flex-col justify-between min-h-screen">
      <div class="space-y-8">
        <div class="flex items-center gap-3 px-2">
          <div class="p-2 bg-slate-900 text-white rounded-lg">
            <Box class="w-5 h-5" />
          </div>
          <span class="font-bold text-slate-800 text-lg">InvSmart</span>
        </div>

        <nav class="space-y-1">
          <button 
            @click="vistaActual = 'productos'" 
            :class="vistaActual === 'productos' ? 'bg-slate-900 text-white shadow-sm' : 'text-slate-500 hover:text-slate-900'"
            class="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl font-medium text-sm transition cursor-pointer"
          >
            <Package class="w-4 h-4" /> Productos
          </button>

          <button 
            @click="vistaActual = 'kardex'" 
            :class="vistaActual === 'kardex' ? 'bg-slate-900 text-white shadow-sm' : 'text-slate-500 hover:text-slate-900'"
            class="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl font-medium text-sm transition cursor-pointer"
          >
            <History class="w-4 h-4" /> Kárdex
          </button>

          <button 
            @click="vistaActual = 'reportes'" 
            :class="vistaActual === 'reportes' ? 'bg-slate-900 text-white shadow-sm' : 'text-slate-500 hover:text-slate-900'"
            class="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl font-medium text-sm transition cursor-pointer"
          >
            <FileText class="w-4 h-4" /> Reportes
          </button>
        </nav>
      </div>

      
    </aside>

    <!-- CONTENIDO PRINCIPAL -->
    <main class="flex-1 p-8 overflow-y-auto">
      
      <header class="flex justify-between items-center mb-8">
        <div class="flex items-center gap-3 bg-white p-1.5 px-3 border border-slate-200 rounded-full">
                      <option value="Administrador">Administrador</option>
        </div>
      </header>

      <!-- VISTA DE PRODUCTOS -->
      <div v-if="vistaActual === 'productos'">
        <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
          <div>
            <h1 class="text-2xl font-bold text-slate-900">Catálogo de Productos</h1>
            <p class="text-xs text-slate-400 mt-1">
              Capital Invertido: <strong class="text-emerald-600">S/. {{ dashboard.valor_inversion || 0 }}</strong>
            </p>
          </div>

          <!-- BOTÓN SOLO VISIBLE PARA ADMINISTRADORES -->
          <div v-if="rolActivo === 'Administrador'" class="flex items-center gap-3">
            <button @click="productoAEditar = null; abrirModal = true" class="px-4 py-2 bg-slate-900 text-white rounded-xl text-sm font-medium hover:bg-slate-800 flex items-center gap-2 shadow-sm cursor-pointer">
              <Plus class="w-4 h-4" /> Añadir Producto
            </button>
          </div>
        </div>

        <!-- FILTROS -->
        <div class="flex justify-between items-center gap-4 mb-6">
          <div class="relative w-72">
            <Search class="w-4 h-4 absolute left-3 top-2.5 text-slate-400" />
            <input v-model="filtroBusqueda" type="text" placeholder="Buscar por nombre o SKU..." class="w-full pl-9 pr-4 py-2 bg-white rounded-xl text-xs border border-slate-200 focus:outline-none" />
          </div>

          <select v-model="categoriaSeleccionada" class="bg-white border border-slate-200 text-xs font-medium rounded-xl px-3 py-2 text-slate-600 focus:outline-none cursor-pointer">
            <option value="">Todas las Categorías</option>
            <option v-for="(val, cat) in dashboard.valor_por_categoria" :key="cat" :value="cat">{{ cat }}</option>
          </select>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          <ProductCard 
            v-for="prod in productosFiltrados" 
            :key="prod.id" 
            :producto="prod" 
            :rol="rolActivo"
            @modificar-stock="modificarStock" 
            @editar-producto="prepararEdicion"
            @eliminar-producto="eliminarProducto"
          />
        </div>
      </div>

      <KardexView v-else-if="vistaActual === 'kardex'" :kardex="kardex" />

      <ReportsView v-else-if="vistaActual === 'reportes'" :dashboard="dashboard" />

    </main>

    <AddProductModal 
      :isOpen="abrirModal" 
      :productoEdit="productoAEditar"
      @close="abrirModal = false; productoAEditar = null" 
      @crear="guardarProducto" 
    />

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { Box, Package, History, FileText, Settings, Search, Plus } from 'lucide-vue-next'
import ProductCard from './components/ProductCard.vue'
import AddProductModal from './components/AddProductModal.vue'
import ReportsView from './components/ReportsView.vue'
import KardexView from './components/KardexView.vue'

const API_URL = 'http://127.0.0.1:8000/api'

const rolActivo = ref('Administrador')
const vistaActual = ref('productos')
const abrirModal = ref(false)
const productoAEditar = ref(null)
const productos = ref([])
const kardex = ref([])
const dashboard = ref({})
const filtroBusqueda = ref('')
const categoriaSeleccionada = ref('')

const cargarDatos = async () => {
  try {
    const resProd = await axios.get(`${API_URL}/productos`)
    const resDash = await axios.get(`${API_URL}/analytics/dashboard`)
    const resKardex = await axios.get(`${API_URL}/kardex`)
    productos.value = resProd.data
    dashboard.value = resDash.data
    kardex.value = resKardex.data
  } catch (err) {
    console.error('Error al cargar datos:', err)
  }
}

const prepararEdicion = (prod) => {
  productoAEditar.value = prod
  abrirModal.value = true
}

const guardarProducto = async (datos) => {
  try {
    if (productoAEditar.value) {
      await axios.put(`${API_URL}/productos/${productoAEditar.value.id}`, datos)
    } else {
      await axios.post(`${API_URL}/productos`, datos)
    }
    abrirModal.value = false
    productoAEditar.value = null
    await cargarDatos()
  } catch (err) {
    alert(err.response?.data?.detail || "Error al procesar producto")
  }
}

const eliminarProducto = async (id) => {
  try {
    await axios.delete(`${API_URL}/productos/${id}`)
    await cargarDatos()
  } catch (err) {
    alert("Error al eliminar producto")
  }
}

const modificarStock = async (id, cantidad) => {
  const motivoIngresado = prompt(
    cantidad > 0 ? "Ingrese el motivo de la ENTRADA de stock:" : "Ingrese el motivo de la SALIDA de stock:",
    cantidad > 0 ? "Compra a proveedor" : "Venta / Despacho"
  )
  if (!motivoIngresado) return

  try {
    await axios.post(`${API_URL}/productos/${id}/movimiento`, { 
      cantidad, 
      motivo: motivoIngresado,
      usuario: rolActivo.value
    })
    await cargarDatos()
  } catch (err) {
    alert(err.response?.data?.detail || "Error al modificar stock")
  }
}

const productosFiltrados = computed(() => {
  return productos.value.filter(p => {
    const coincideBusqueda = p.nombre.toLowerCase().includes(filtroBusqueda.value.toLowerCase()) || p.sku.toLowerCase().includes(filtroBusqueda.value.toLowerCase())
    const coincideCat = categoriaSeleccionada.value === '' || p.categoria === categoriaSeleccionada.value
    return coincideBusqueda && coincideCat
  })
})

onMounted(() => {
  cargarDatos()
})
</script>