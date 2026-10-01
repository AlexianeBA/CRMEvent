<template>
  <DashboardLayout>
    <div class="page-header">
      <div><h1>Factures</h1><p>Gestion des factures issues des devis acceptés</p></div>
      <v-btn variant="tonal" prepend-icon="mdi-microsoft-excel" :loading="exporting" @click="exportExcel">Exporter en Excel</v-btn>
    </div>
    <InvoiceTable />
  </DashboardLayout>
</template>

<script setup>
import { ref } from "vue"
import DashboardLayout from "@/layouts/DashboardLayout.vue"
import InvoiceTable from "@/components/invoice/InvoiceTable.vue"
import invoiceService from "@/services/invoiceService"
import { downloadResponse } from "@/utils/download"

const exporting = ref(false)
async function exportExcel() {
  exporting.value = true
  try { downloadResponse(await invoiceService.exportExcel(), "factures.xlsx") }
  catch (error) { window.alert(error.response?.data?.detail ?? "Impossible d’exporter les factures") }
  finally { exporting.value = false }
}
</script>

<style scoped>
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
</style>
