<template>
  <div class="details-grid">
    <DetailsCard title="Informations du devis" icon="mdi-file-document-outline" :item="quote" :fields="generalFields">
      <template #field-status="{ value }">
        <v-chip :color="statusColor(value)" variant="tonal" size="small">{{ statusLabel(value) }}</v-chip>
      </template>
    </DetailsCard>

    <DetailsCard title="Relations" icon="mdi-link-variant" :item="quote" :fields="relationFields">
      <template #field-company="{ item }">
        <RouterLink :to="{ name: 'CompanyView', params: { id: item.company.id } }" class="detail-link">{{ item.company.name }}</RouterLink>
      </template>
      <template #field-event="{ item }">
        <RouterLink v-if="item.event" :to="{ name: 'EventView', params: { id: item.event.id } }" class="detail-link">{{ item.event.title }}</RouterLink>
        <strong v-else>—</strong>
      </template>
    </DetailsCard>
  </div>
</template>

<script setup>
import DetailsCard from "@/components/common/DetailsCard.vue"

defineProps({ quote: { type: Object, required: true } })

const labels = { draft: "Brouillon", sent: "Envoyé", accepted: "Accepté", rejected: "Refusé", expired: "Expiré", locked: "Verrouillé" }
const colors = { draft: "grey", sent: "blue", accepted: "green", rejected: "red", expired: "orange", locked: "purple" }

const generalFields = [
  { key: "number", label: "Numéro" },
  { key: "title", label: "Titre" },
  { key: "total_amount", label: "Montant total", formatter: (value) => new Intl.NumberFormat("fr-FR", { style: "currency", currency: "EUR" }).format(Number(value ?? 0)) },
  { key: "status", label: "Statut" },
]

const relationFields = [
  { key: "company", label: "Entreprise", value: (item) => item.company?.name },
  { key: "opportunity", label: "Opportunité", value: (item) => item.opportunity?.title },
  { key: "assigned_user", label: "Utilisateur assigné", value: (item) => item.assigned_user?.email },
  { key: "event", label: "Événement", value: (item) => item.event?.title },
]

function statusLabel(status) { return labels[status] ?? status }
function statusColor(status) { return colors[status] ?? "grey" }
</script>

<style scoped>
.details-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 24px; }
.detail-link { color: #2563eb; font-weight: 600; text-decoration: none; }
.detail-link:hover { text-decoration: underline; }
@media (max-width: 850px) { .details-grid { grid-template-columns: 1fr; } }
</style>
