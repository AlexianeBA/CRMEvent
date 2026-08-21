<template>
  <section class="card">
    <div class="card-header"><div><h3>Pipeline commercial</h3><p>Répartition des opportunités</p></div><v-btn variant="text" size="small" @click="router.push({ name: 'Opportunities' })">Voir tout</v-btn></div>
    <v-progress-linear v-if="loading" indeterminate />
    <div v-else class="pipeline">
      <div v-for="stage in stages" :key="stage.status" class="stage">
        <div class="stage-line"><span>{{ stage.label }}</span><strong>{{ stage.count }}</strong></div>
        <v-progress-linear :model-value="stage.percentage" :color="stage.color" height="8" rounded />
        <small>{{ formatCurrency(stage.amount) }}</small>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed } from "vue"
import { useRouter } from "vue-router"
const props = defineProps({ loading: Boolean, opportunities: { type: Array, default: () => [] } })
const router = useRouter()
const definitions = [
  ["new", "Nouvelles", "blue-grey"], ["qualification", "Qualification", "blue"], ["proposal", "Proposition", "cyan"],
  ["negotiation", "Négociation", "orange"], ["closed_won", "Gagnées", "green"], ["closed_lost", "Perdues", "red"],
]
const stages = computed(() => definitions.map(([status, label, color]) => {
  const items = props.opportunities.filter((item) => item.status === status)
  return { status, label, color, count: items.length, amount: items.reduce((sum, item) => sum + Number(item.amount ?? 0), 0), percentage: props.opportunities.length ? items.length / props.opportunities.length * 100 : 0 }
}))
function formatCurrency(value) { return new Intl.NumberFormat("fr-FR", { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(value) }
</script>

<style scoped>
.card { background: white; border-radius: 14px; padding: 24px; }.card-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 22px; }
h3, p { margin: 0; }p { color: #64748b; font-size: 13px; margin-top: 4px; }.pipeline { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px 28px; }
.stage-line { display: flex; justify-content: space-between; margin-bottom: 7px; }.stage small { display: block; color: #64748b; margin-top: 6px; }
@media (max-width: 650px) { .pipeline { grid-template-columns: 1fr; } }
</style>
