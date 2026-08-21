<template>
  <DashboardLayout>
    <div class="page-header">
      <div><h1>Factures</h1><p>Gestion des factures issues des devis acceptés</p></div>
    </div>
    <InvoiceTable />
  </DashboardLayout>
</template>

<script setup>
import DashboardLayout from "@/layouts/DashboardLayout.vue"
import InvoiceTable from "@/components/invoice/InvoiceTable.vue"
</script>

<style scoped>
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
</style>
