<template>
  <DataTable ref="table" resource="invoices" :columns="columns">
    <template #cell-status="{ value }">
      <v-chip :color="statusColor(value)" size="small" variant="tonal">{{
        statusLabel(value)
      }}</v-chip>
    </template>
    <template #actions="{ item }">
      <div class="action-buttons">
        <v-btn
          icon="mdi-eye-outline"
          variant="text"
          size="small"
          title="Voir la facture"
          @click.stop="viewInvoice(item)"
        />
        <v-btn
          v-if="auth.canManageInvoices"
          icon="mdi-pencil-outline"
          variant="text"
          size="small"
          title="Modifier la facture"
          :disabled="!canEdit(item)"
          @click.stop="editInvoice(item)"
        />
        <v-btn
          v-if="auth.canManageInvoices"
          icon="mdi-delete-outline"
          variant="text"
          size="small"
          color="error"
          title="Supprimer la facture"
          :disabled="!canDelete(item)"
          @click.stop="deleteInvoice(item)"
        />
      </div>
    </template>
  </DataTable>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import DataTable from '@/components/common/DataTable.vue'
import invoiceService from '@/services/invoiceService'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const table = ref(null)
const auth = useAuthStore()

const labels = {
  draft: 'Brouillon',
  sent: 'Envoyée',
  paid: 'Payée',
  overdue: 'En retard',
  canceled: 'Annulée',
  locked: 'Verrouillée',
}
const colors = {
  draft: 'grey',
  sent: 'blue',
  paid: 'green',
  overdue: 'orange',
  canceled: 'red',
  locked: 'purple',
}
const columns = [
  { key: 'number', label: 'Numéro' },
  { key: 'title', label: 'Titre' },
  {
    key: 'total_amount',
    label: 'Montant HT',
    formatter: (value) =>
      new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR' }).format(
        Number(value ?? 0),
      ),
  },
  {
    key: 'total_incl_tax',
    label: 'Montant TTC',
    formatter: (value) =>
      new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR' }).format(
        Number(value ?? 0),
      ),
  },
  {
    key: 'balance_remaining',
    label: 'Solde',
    formatter: (value) =>
      new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR' }).format(
        Number(value ?? 0),
      ),
  },
  {
    key: 'due_date',
    label: 'Échéance',
    formatter: (value) =>
      value
        ? new Intl.DateTimeFormat('fr-FR', { dateStyle: 'short' }).format(new Date(value))
        : '—',
  },
  { key: 'status', label: 'Statut' },
]

const statusLabel = (status) => labels[status] ?? status
const statusColor = (status) => colors[status] ?? 'grey'
const canEdit = (invoice) => ['draft', 'sent', 'overdue'].includes(invoice.status)
const canDelete = (invoice) => ['draft', 'canceled'].includes(invoice.status)
const viewInvoice = (invoice) => router.push({ name: 'InvoiceView', params: { id: invoice.id } })
const editInvoice = (invoice) => router.push({ name: 'InvoiceEdit', params: { id: invoice.id } })

async function deleteInvoice(invoice) {
  if (!window.confirm(`Supprimer la facture ${invoice.number} ?`)) return
  try {
    await invoiceService.delete(invoice.id)
    table.value?.reload()
  } catch (error) {
    window.alert(error.response?.data?.detail ?? 'Impossible de supprimer la facture')
  }
}
</script>

<style scoped>
.action-buttons {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 4px;
}
</style>
