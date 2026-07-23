<template>
  <aside class="w-64 bg-slate-50 border-r border-slate-200 p-6 flex flex-col justify-between min-h-screen">
    <div class="space-y-8">
      <!-- Logo -->
      <div class="flex items-center gap-3 px-2">
        <div class="p-2 bg-slate-900 text-white rounded-lg">
          <Box class="w-5 h-5" />
        </div>
        <span class="font-bold text-slate-800 text-lg">Inventory</span>
      </div>

      <!-- Menú de Navegación -->
      <nav class="space-y-1">
        <a href="#" class="flex items-center justify-between px-3 py-2.5 text-slate-500 hover:text-slate-900 rounded-xl font-medium text-sm transition">
          <div class="flex items-center gap-3"><LayoutDashboard class="w-4 h-4" /> Dashboard</div>
        </a>
        
        <!-- Opción Activa (Products) -->
        <a href="#" class="flex items-center justify-between px-3 py-2.5 bg-slate-900 text-white rounded-xl font-medium text-sm shadow-sm">
          <div class="flex items-center gap-3"><Package class="w-4 h-4" /> Products</div>
        </a>

        <a href="#" class="flex items-center justify-between px-3 py-2.5 text-slate-500 hover:text-slate-900 rounded-xl font-medium text-sm transition">
          <div class="flex items-center gap-3"><FileText class="w-4 h-4" /> Reports</div>
        </a>
      </nav>
    </div>

    <!-- Menú Inferior -->
    <div class="space-y-1 pt-6 border-t border-slate-200">
      <a href="#" class="flex items-center gap-3 px-3 py-2.5 text-slate-500 hover:text-slate-900 rounded-xl font-medium text-sm">
        <Settings class="w-4 h-4" /> Settings
      </a>
      <a href="#" class="flex items-center gap-3 px-3 py-2.5 text-rose-500 hover:bg-rose-50 rounded-xl font-medium text-sm">
        <LogOut class="w-4 h-4" /> Logout
      </a>
    </div>
  </aside>
</template>

<script setup>
import { Box, LayoutDashboard, Package, FileText, Settings, LogOut } from 'lucide-vue-next'
</script>