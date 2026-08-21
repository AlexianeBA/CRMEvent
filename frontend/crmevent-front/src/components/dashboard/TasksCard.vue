<template>
  <section class="card">
    <div class="card-header"><div><h3>À traiter</h3><p>Actions commerciales prioritaires</p></div><v-chip color="error" variant="tonal" size="small">{{ total }}</v-chip></div>
    <v-progress-linear v-if="loading" indeterminate />
    <div v-else-if="tasks.length" class="task-list">
      <button v-for="task in tasks" :key="task.label" type="button" @click="router.push({ name: task.route })">
        <v-avatar :color="task.color" variant="tonal" size="38"><v-icon :icon="task.icon" size="20" /></v-avatar>
        <span><strong>{{ task.count }} {{ task.label }}</strong><small>{{ task.hint }}</small></span>
        <v-icon icon="mdi-chevron-right" color="grey" />
      </button>
    </div>
    <p v-else class="empty">Aucune action urgente</p>
  </section>
</template>

<script setup>
import { computed } from "vue"
import { useRouter } from "vue-router"
const props = defineProps({ loading: Boolean, events: { type: Array, default: () => [] }, quotes: { type: Array, default: () => [] }, invoices: { type: Array, default: () => [] } })
const router = useRouter()
const tasks = computed(() => [
  { label: "devis en brouillon", count: props.quotes.filter((item) => item.status === "draft").length, hint: "À vérifier ou envoyer", route: "Quotes", icon: "mdi-file-edit-outline", color: "blue" },
  { label: "factures en retard", count: props.invoices.filter((item) => item.status === "overdue").length, hint: "Relance recommandée", route: "Invoices", icon: "mdi-alert-circle-outline", color: "error" },
  { label: "factures à envoyer", count: props.invoices.filter((item) => item.status === "draft").length, hint: "Encore en brouillon", route: "Invoices", icon: "mdi-email-fast-outline", color: "orange" },
  { label: "événements à planifier", count: props.events.filter((item) => item.status === "draft").length, hint: "Statut brouillon", route: "Events", icon: "mdi-calendar-clock", color: "purple" },
].filter((task) => task.count > 0))
const total = computed(() => tasks.value.reduce((sum, task) => sum + task.count, 0))
</script>

<style scoped>
.card { background: white; border-radius: 14px; padding: 22px; }.card-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 16px; }
h3, p { margin: 0; }.card-header p { color: #64748b; font-size: 13px; margin-top: 4px; }.task-list { display: flex; flex-direction: column; }
.task-list button { display: flex; align-items: center; gap: 12px; width: 100%; padding: 12px 0; border: 0; border-bottom: 1px solid #eef2f7; background: transparent; text-align: left; cursor: pointer; }
.task-list button span { min-width: 0; flex: 1; }.task-list strong, .task-list small { display: block; }.task-list small { color: #64748b; margin-top: 2px; }.empty { padding: 24px 0; color: #64748b; text-align: center; }
</style>
