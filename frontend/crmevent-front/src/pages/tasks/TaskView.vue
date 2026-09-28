<template>
  <DashboardLayout>
    <DetailPage :title="task?.title || 'Tâche'" breadcrumb="Tâches / Détail" :loading="loading" :error="error" :show-edit="canManage && canChange" @back="router.push({ name: 'Tasks' })" @edit="router.push({ name: 'TaskEdit', params: { id: task.id } })">
      <template #actions>
        <v-btn v-if="task?.status === 'todo'" color="primary" :loading="saving" @click="changeStatus('in_progress')">Commencer</v-btn>
        <v-btn v-if="['todo', 'in_progress'].includes(task?.status)" color="success" :loading="saving" @click="changeStatus('done')">Terminer</v-btn>
        <v-btn v-if="canManage && canChange" color="warning" variant="tonal" :loading="saving" @click="changeStatus('canceled')">Annuler</v-btn>
        <v-btn v-if="canManage" color="error" variant="tonal" :loading="saving" @click="deleteTask">Supprimer</v-btn>
      </template>
      <v-card v-if="task" class="pa-6">
        <div class="task-heading"><v-chip :color="statusColors[task.status]" variant="tonal">{{ statusLabels[task.status] }}</v-chip><v-chip :color="priorityColors[task.priority]" variant="tonal">Priorité {{ priorityLabels[task.priority].toLowerCase() }}</v-chip></div>
        <p class="description">{{ task.description || "Aucune description" }}</p>
        <v-list>
          <v-list-item prepend-icon="mdi-account-outline" title="Assignée à" :subtitle="task.assigned_user.email" />
          <v-list-item prepend-icon="mdi-calendar-clock" title="Échéance" :subtitle="formatDate(task.due_at)" />
          <v-list-item v-if="task.opportunity" prepend-icon="mdi-briefcase-outline" title="Opportunité" :subtitle="task.opportunity.title" @click="router.push(`/opportunities/${task.opportunity.id}`)" />
          <v-list-item v-if="task.event" prepend-icon="mdi-calendar-outline" title="Événement" :subtitle="task.event.title" @click="router.push(`/events/${task.event.id}`)" />
        </v-list>
      </v-card>
    </DetailPage>
  </DashboardLayout>
</template>

<script setup>
import { computed, onMounted, ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import DashboardLayout from "@/layouts/DashboardLayout.vue"
import DetailPage from "@/components/common/DetailPage.vue"
import taskService from "@/services/taskService"
import { useAuthStore } from "@/stores/auth"

defineOptions({ name: "TaskViewPage" })
const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const task = ref(null)
const loading = ref(false)
const saving = ref(false)
const error = ref("")
const canChange = computed(() => !["done", "canceled"].includes(task.value?.status))
const canManage = computed(() => ["admin", "manager"].includes(auth.user?.role) || task.value?.created_by_id === auth.user?.id)
const statusLabels = { todo: "À faire", in_progress: "En cours", done: "Terminée", canceled: "Annulée" }
const statusColors = { todo: "grey", in_progress: "blue", done: "success", canceled: "warning" }
const priorityLabels = { low: "Faible", medium: "Normale", high: "Haute" }
const priorityColors = { low: "grey", medium: "primary", high: "error" }

async function loadTask() {
  loading.value = true
  try { task.value = await taskService.getById(route.params.id) }
  catch (err) { error.value = err.response?.data?.detail ?? "Impossible de charger la tâche" }
  finally { loading.value = false }
}
async function changeStatus(status) {
  saving.value = true
  try { task.value = await taskService.update(task.value.id, { status }) }
  catch (err) { error.value = err.response?.data?.detail ?? "Impossible de modifier la tâche" }
  finally { saving.value = false }
}
async function deleteTask() {
  if (!window.confirm("Supprimer cette tâche ?")) return
  saving.value = true
  try { await taskService.delete(task.value.id); await router.push({ name: "Tasks" }) }
  catch (err) { error.value = err.response?.data?.detail ?? "Impossible de supprimer la tâche" }
  finally { saving.value = false }
}
const formatDate = (value) => new Intl.DateTimeFormat("fr-FR", { dateStyle: "medium", timeStyle: "short" }).format(new Date(value))
onMounted(loadTask)
</script>

<style scoped>
.task-heading { display: flex; gap: 10px; }
.description { margin: 24px 0; white-space: pre-wrap; }
</style>
