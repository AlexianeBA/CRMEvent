<template>
  <div class="details-grid">
    <DetailsCard title="Informations de la facture" icon="mdi-receipt-text-outline" :item="invoice" :fields="generalFields">
      <template #field-status="{ value }">
        <v-chip :color="statusColor(value)" variant="tonal" size="small">{{ statusLabel(value) }}</v-chip>
      </template>
    </DetailsCard>
    <DetailsCard title="Relations" icon="mdi-link-variant" :item="invoice" :fields="relationFields">
      <template #field-company="{ item }">
        <RouterLink :to="{ name: 'CompanyView', params: { id: item.company.id } }" class="detail-link">{{ item.company.name }}</RouterLink>
      </template>
      <template #field-quote="{ item }">
        <RouterLink :to="{ name: 'QuoteView', params: { id: item.quote.id } }" class="detail-link">{{ item.quote.number }} — {{ item.quote.title }}</RouterLink>
      </template>
    </DetailsCard>
  </div>
</template>

<script setup>
import DetailsCard from "@/components/common/DetailsCard.vue"

defineProps({ invoice: { type: Object, required: true } })
const labels = { draft: "Brouillon", sent: "Envoyée", paid: "Payée", overdue: "En retard", canceled: "Annulée", locked: "Verrouillée" }
const colors = { draft: "grey", sent: "blue", paid: "green", overdue: "orange", canceled: "red", locked: "purple" }
const dateFormatter = (value) => value ? new Intl.DateTimeFormat("fr-FR", { dateStyle: "medium", timeStyle: "short" }).format(new Date(value)) : "—"
const generalFields = [
  { key: "number", label: "Numéro" },
  { key: "title", label: "Titre" },
  { key: "total_amount", label: "Montant total", formatter: (value) => new Intl.NumberFormat("fr-FR", { style: "currency", currency: "EUR" }).format(Number(value ?? 0)) },
  { key: "status", label: "Statut" },
  { key: "created_at", label: "Créée le", formatter: dateFormatter },
  { key: "updated_at", label: "Modifiée le", formatter: dateFormatter },
]
const relationFields = [
  { key: "company", label: "Entreprise", value: (item) => item.company?.name },
  { key: "quote", label: "Devis", value: (item) => item.quote?.number },
  { key: "opportunity", label: "Opportunité", value: (item) => item.opportunity?.title },
  { key: "assigned_user", label: "Utilisateur assigné", value: (item) => item.assigned_user?.email },
]
const statusLabel = (status) => labels[status] ?? status
const statusColor = (status) => colors[status] ?? "grey"
</script>

<style scoped>
.details-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 24px; }
.detail-link { color: #2563eb; font-weight: 600; text-decoration: none; }
.detail-link:hover { text-decoration: underline; }
@media (max-width: 850px) { .details-grid { grid-template-columns: 1fr; } }
</style>
