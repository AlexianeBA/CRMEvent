<template>
  <DashboardLayout>

    <div class="page-header">
      <div>
        <h1>Devis</h1>
        <p>Gestion des devis clients</p>
      </div>

      <div class="page-actions">
        <v-btn variant="tonal" prepend-icon="mdi-microsoft-excel" :loading="exporting" @click="exportExcel">Exporter en Excel</v-btn>
        <v-btn v-if="auth.canManageCrm" color="primary" prepend-icon="mdi-plus" @click="goToCreate">Nouveau devis</v-btn>
      </div>
    </div>

    <QuoteTable />

  </DashboardLayout>
</template>

<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import DashboardLayout from "@/layouts/DashboardLayout.vue"
import QuoteTable from "@/components/quotes/QuoteTable.vue"
import { useAuthStore } from "@/stores/auth"
import quoteService from "@/services/quotesService"
import { downloadResponse } from "@/utils/download"

const router = useRouter()
const auth = useAuthStore()
const exporting = ref(false)

async function exportExcel() {
  exporting.value = true
  try { downloadResponse(await quoteService.exportExcel(), "devis.xlsx") }
  catch (error) { window.alert(error.response?.data?.detail ?? "Impossible d’exporter les devis") }
  finally { exporting.value = false }
}

function goToCreate() {
  router.push({
    name: "QuoteCreate",
  })
}
</script>

<style scoped>

.page-header{
display:flex;
justify-content:space-between;
align-items:center;
margin-bottom:30px;
}
.page-actions { display: flex; gap: 10px; }

.btn-primary{
background:#3B82F6;
color:white;
padding:12px 20px;
border:none;
border-radius:8px;
cursor:pointer;
}

</style>
