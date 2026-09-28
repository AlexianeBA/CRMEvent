<template>
  <DashboardLayout>
    <div class="page-header">
      <div><h1>Tâches</h1><p>Suivi des actions assignées et de leurs échéances</p></div>
      <v-btn color="primary" prepend-icon="mdi-plus" :to="{ name: 'TaskCreate' }">Nouvelle tâche</v-btn>
    </div>
    <v-alert v-if="error" type="error" variant="tonal" class="mb-4">{{ error }}</v-alert>
    <DataTable :items="tasks" :columns="columns" :search-fields="['title', 'status', 'priority']" :loading="loading">
      <template #cell-status="{ value }"><v-chip :color="statusColors[value]" size="small" variant="tonal">{{ statusLabels[value] }}</v-chip></template>
      <template #cell-priority="{ value }"><v-chip :color="priorityColors[value]" size="small" variant="tonal">{{ priorityLabels[value] }}</v-chip></template>
      <template #actions="{ item }">
        <v-btn icon="mdi-eye-outline" variant="text" size="small" title="Voir" @click.stop="router.push({ name: 'TaskView', params: { id: item.id } })" />
      </template>
    </DataTable>
  </DashboardLayout>
</template>

<script setup>
import { onMounted, ref } from "vue"
import { useRouter } from "vue-router"
import DashboardLayout from "@/layouts/DashboardLayout.vue"
import DataTable from "@/components/common/DataTable.vue"
import taskService from "@/services/taskService"

defineOptions({ name: "TaskListPage" })
const router = useRouter()
const tasks = ref([])
const loading = ref(false)
const error = ref("")
const statusLabels = { todo: "À faire", in_progress: "En cours", done: "Terminée", canceled: "Annulée" }
const statusColors = { todo: "grey", in_progress: "blue", done: "success", canceled: "warning" }
const priorityLabels = { low: "Faible", medium: "Normale", high: "Haute" }
const priorityColors = { low: "grey", medium: "primary", high: "error" }
const columns = [
  { key: "title", label: "Titre" },
  { key: "priority", label: "Priorité" },
  { key: "status", label: "Statut" },
  { key: "assigned_user", label: "Assignée à", formatter: (value) => value?.email ?? "—" },
  { key: "due_at", label: "Échéance", formatter: (value) => new Intl.DateTimeFormat("fr-FR", { dateStyle: "short", timeStyle: "short" }).format(new Date(value)) },
]

async function loadTasks() {
  loading.value = true
  try { tasks.value = await taskService.list() }
  catch (err) { error.value = err.response?.data?.detail ?? "Impossible de charger les tâches" }
  finally { loading.value = false }
}
onMounted(loadTasks)
</script>

<style scoped>
.page-header { display: flex; justify-content: space-between; align-items: center; gap: 20px; margin-bottom: 30px; }
.page-header h1, .page-header p { margin: 0; }
.page-header p { color: #6b7280; }
@media (max-width: 700px) { .page-header { align-items: stretch; flex-direction: column; } }
</style>
