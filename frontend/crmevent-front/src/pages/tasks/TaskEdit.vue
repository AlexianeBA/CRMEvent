<template>
  <DashboardLayout>
    <div v-if="loading" class="state">Chargement...</div>
    <EditPage v-else title="Modifier la tâche" breadcrumb="Tâches / Modification" :saving="saving" :error="error" @submit="submit" @cancel="goBack">
      <TaskForm ref="formRef" v-model="form" />
    </EditPage>
  </DashboardLayout>
</template>

<script setup>
import { onMounted, reactive, ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import DashboardLayout from "@/layouts/DashboardLayout.vue"
import EditPage from "@/components/common/EditPage.vue"
import TaskForm from "@/components/task/TaskForm.vue"
import taskService from "@/services/taskService"

defineOptions({ name: "TaskEditPage" })
const route = useRoute()
const router = useRouter()
const formRef = ref(null)
const loading = ref(false)
const saving = ref(false)
const error = ref("")
const form = reactive({ title: "", description: "", priority: "medium", dueAt: "", assignedUserId: null, opportunityId: null, eventId: null })

async function loadTask() {
  loading.value = true
  try {
    const task = await taskService.getById(route.params.id)
    Object.assign(form, { title: task.title, description: task.description ?? "", priority: task.priority, dueAt: new Date(task.due_at).toISOString().slice(0, 16), assignedUserId: task.assigned_user_id, opportunityId: task.opportunity_id, eventId: task.event_id })
  } catch (err) { error.value = err.response?.data?.detail ?? "Impossible de charger la tâche" }
  finally { loading.value = false }
}

async function submit() {
  if (!(await formRef.value?.validate())) return
  saving.value = true
  try {
    await taskService.update(route.params.id, { title: form.title.trim(), description: form.description?.trim() || null, priority: form.priority, due_at: new Date(form.dueAt).toISOString(), assigned_user_id: Number(form.assignedUserId), opportunity_id: form.opportunityId ? Number(form.opportunityId) : null, event_id: form.eventId ? Number(form.eventId) : null })
    await goBack()
  } catch (err) { error.value = err.response?.data?.detail ?? "Impossible de modifier la tâche" }
  finally { saving.value = false }
}
function goBack() { return router.push({ name: "TaskView", params: { id: route.params.id } }) }
onMounted(loadTask)
</script>

<style scoped>.state { padding: 48px; text-align: center; }</style>
