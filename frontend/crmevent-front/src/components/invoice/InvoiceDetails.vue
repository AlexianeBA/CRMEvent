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
  <v-card class="mt-6" rounded="xl" elevation="0" border><v-card-title>Lignes facturées</v-card-title><v-table><thead><tr><th>Description</th><th>Quantité</th><th>Prix HT</th><th>Remise</th><th>TVA</th><th>Total HT</th></tr></thead><tbody><tr v-for="line in invoice.lines" :key="line.id"><td>{{ line.description }}</td><td>{{ line.quantity }} {{ line.unit }}</td><td>{{ currencyFormatter(line.unit_price_excl_tax) }}</td><td>{{ line.discount_rate }} %</td><td>{{ line.vat_rate }} %</td><td>{{ currencyFormatter(line.total_excl_tax) }}</td></tr></tbody></v-table></v-card>
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
  { key: "total_amount", label: "Montant HT", formatter: currencyFormatter },
  { key: "vat_rate", label: "Taux de TVA", formatter: (value) => `${Number(value ?? 0)} %` },
  { key: "vat_amount", label: "Montant TVA", formatter: currencyFormatter },
  { key: "total_incl_tax", label: "Montant TTC", formatter: currencyFormatter },
  { key: "amount_paid", label: "Montant payé", formatter: currencyFormatter },
  { key: "balance_remaining", label: "Solde restant", formatter: currencyFormatter },
  { key: "status", label: "Statut" },
  { key: "issue_date", label: "Date d’émission", formatter: dateFormatter },
  { key: "due_date", label: "Échéance", formatter: dateFormatter },
  { key: "payment_terms", label: "Conditions de paiement" },
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
function currencyFormatter(value) { return new Intl.NumberFormat("fr-FR", { style: "currency", currency: "EUR" }).format(Number(value ?? 0)) }
</script>

<style scoped>
.details-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 24px; }
.detail-link { color: #2563eb; font-weight: 600; text-decoration: none; }
.detail-link:hover { text-decoration: underline; }
@media (max-width: 850px) { .details-grid { grid-template-columns: 1fr; } }
</style>
