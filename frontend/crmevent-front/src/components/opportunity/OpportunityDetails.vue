<template>
  <div class="details-grid">
    <DetailsCard title="Informations" icon="mdi-briefcase-outline" :item="opportunity" :fields="generalFields">
      <template #field-status="{ value }"><v-chip :color="statusColor(value)" variant="tonal" size="small">{{ statusLabel(value) }}</v-chip></template>
    </DetailsCard>
    <DetailsCard title="Relations" icon="mdi-link-variant" :item="opportunity" :fields="relationFields">
      <template #field-company="{ item }"><RouterLink :to="{ name: 'CompanyView', params: { id: item.company.id } }" class="detail-link">{{ item.company.name }}</RouterLink></template>
      <template #field-contact="{ item }"><RouterLink :to="{ name: 'ContactView', params: { id: item.contact.id } }" class="detail-link">{{ item.contact.first_name }} {{ item.contact.last_name }}</RouterLink></template>
    </DetailsCard>
  </div>
</template>

<script setup>
import DetailsCard from "@/components/common/DetailsCard.vue"

defineProps({ opportunity: { type: Object, required: true } })
const labels = { new: "Nouvelle", qualification: "Qualification", proposal: "Proposition", negotiation: "Négociation", closed_won: "Gagnée", closed_lost: "Perdue" }
const colors = { new: "blue-grey", qualification: "blue", proposal: "cyan", negotiation: "orange", closed_won: "green", closed_lost: "red" }
const generalFields = [
  { key: "title", label: "Titre" },
  { key: "amount", label: "Montant", formatter: (value) => new Intl.NumberFormat("fr-FR", { style: "currency", currency: "EUR" }).format(Number(value ?? 0)) },
  { key: "status", label: "Statut" },
  { key: "created_at", label: "Créée le", formatter: (value) => formatDate(value) },
  { key: "updated_at", label: "Modifiée le", formatter: (value) => formatDate(value) },
]
const relationFields = [
  { key: "company", label: "Entreprise", value: (item) => item.company?.name },
  { key: "contact", label: "Contact", value: (item) => `${item.contact?.first_name ?? ""} ${item.contact?.last_name ?? ""}`.trim() },
  { key: "commercial", label: "Commercial", value: (item) => item.commercial?.email },
]
const statusLabel = (status) => labels[status] ?? status
const statusColor = (status) => colors[status] ?? "grey"
function formatDate(value) { return value ? new Intl.DateTimeFormat("fr-FR", { dateStyle: "medium", timeStyle: "short" }).format(new Date(value)) : "—" }
</script>

<style scoped>
.details-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 24px; }
.detail-link { color: #2563eb; font-weight: 600; text-decoration: none; }
.detail-link:hover { text-decoration: underline; }
@media (max-width: 850px) { .details-grid { grid-template-columns: 1fr; } }
</style>
