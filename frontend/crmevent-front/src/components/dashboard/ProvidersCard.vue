<template>
  <section class="card">
    <div class="card-header"><div><h3>Suivi financier</h3><p>Devis et facturation</p></div><v-icon icon="mdi-chart-box-outline" color="primary" /></div>
    <v-progress-linear v-if="loading" indeterminate />
    <div v-else class="financial-list">
      <div><span>Devis acceptés</span><strong>{{ formatCurrency(acceptedQuotes) }}</strong></div>
      <div><span>Facturé</span><strong>{{ formatCurrency(invoicedAmount) }}</strong></div>
      <div><span>Encaissé</span><strong class="success">{{ formatCurrency(paidAmount) }}</strong></div>
      <div><span>À encaisser</span><strong class="warning">{{ formatCurrency(outstandingAmount) }}</strong></div>
    </div>
    <v-btn variant="tonal" color="primary" block class="mt-4" @click="router.push({ name: 'Invoices' })">Voir les factures</v-btn>
  </section>
</template>

<script setup>
import { computed } from "vue"
import { useRouter } from "vue-router"
const props = defineProps({ loading: Boolean, quotes: { type: Array, default: () => [] }, invoices: { type: Array, default: () => [] } })
const router = useRouter()
const acceptedQuotes = computed(() => props.quotes.filter((item) => ["accepted", "locked"].includes(item.status)).reduce((sum, item) => sum + Number(item.total_amount ?? 0), 0))
const invoicedAmount = computed(() => props.invoices.filter((item) => item.status !== "canceled").reduce((sum, item) => sum + Number(item.total_amount ?? 0), 0))
const paidAmount = computed(() => props.invoices.filter((item) => ["paid", "locked"].includes(item.status)).reduce((sum, item) => sum + Number(item.total_amount ?? 0), 0))
const outstandingAmount = computed(() => props.invoices.filter((item) => ["draft", "sent", "overdue"].includes(item.status)).reduce((sum, item) => sum + Number(item.total_amount ?? 0), 0))
function formatCurrency(value) { return new Intl.NumberFormat("fr-FR", { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(value) }
</script>

<style scoped>
.card { background: white; border-radius: 14px; padding: 22px; }.card-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px; }
h3, p { margin: 0; }p { color: #64748b; font-size: 13px; margin-top: 4px; }.financial-list { display: flex; flex-direction: column; }
.financial-list div { display: flex; justify-content: space-between; gap: 16px; padding: 13px 0; border-bottom: 1px solid #eef2f7; }.financial-list span { color: #64748b; }.success { color: #15803d; }.warning { color: #c2410c; }
</style>
