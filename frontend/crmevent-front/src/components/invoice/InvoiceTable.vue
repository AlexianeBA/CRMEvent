<template>
  <DataTable :items="store.invoices" :columns="columns" :search-fields="['number', 'title', 'status']" :loading="store.loading">
    <template #cell-status="{ value }">
      <v-chip :color="statusColor(value)" size="small" variant="tonal">{{ statusLabel(value) }}</v-chip>
    </template>
    <template #actions="{ item }">
      <div class="action-buttons">
        <v-btn icon="mdi-eye-outline" variant="text" size="small" title="Voir la facture" @click.stop="viewInvoice(item)" />
        <v-btn icon="mdi-pencil-outline" variant="text" size="small" title="Modifier la facture" :disabled="!canEdit(item)" @click.stop="editInvoice(item)" />
        <v-btn icon="mdi-delete-outline" variant="text" size="small" color="error" title="Supprimer la facture" :disabled="!canDelete(item)" @click.stop="deleteInvoice(item)" />
      </div>
    </template>
  </DataTable>
</template>

<script setup>
import { onMounted } from "vue"
import { useRouter } from "vue-router"
import DataTable from "@/components/common/DataTable.vue"
import { useInvoiceStore } from "@/stores/invoice"

const router = useRouter()
const store = useInvoiceStore()

const labels = { draft: "Brouillon", sent: "Envoyée", paid: "Payée", overdue: "En retard", canceled: "Annulée", locked: "Verrouillée" }
const colors = { draft: "grey", sent: "blue", paid: "green", overdue: "orange", canceled: "red", locked: "purple" }
const columns = [
  { key: "number", label: "Numéro" },
  { key: "title", label: "Titre" },
  { key: "total_amount", label: "Montant", formatter: (value) => new Intl.NumberFormat("fr-FR", { style: "currency", currency: "EUR" }).format(Number(value ?? 0)) },
  { key: "status", label: "Statut" },
]

const statusLabel = (status) => labels[status] ?? status
const statusColor = (status) => colors[status] ?? "grey"
const canEdit = (invoice) => ["draft", "sent", "overdue"].includes(invoice.status)
const canDelete = (invoice) => ["draft", "canceled"].includes(invoice.status)
const viewInvoice = (invoice) => router.push({ name: "InvoiceView", params: { id: invoice.id } })
const editInvoice = (invoice) => router.push({ name: "InvoiceEdit", params: { id: invoice.id } })

async function deleteInvoice(invoice) {
  if (!window.confirm(`Supprimer la facture ${invoice.number} ?`)) return
  try {
    await store.deleteInvoice(invoice.id)
  } catch (error) {
    window.alert(error.response?.data?.detail ?? "Impossible de supprimer la facture")
  }
}

onMounted(() => store.loadInvoices())
</script>

<style scoped>
.action-buttons { display: flex; align-items: center; justify-content: flex-end; gap: 4px; }
</style>
