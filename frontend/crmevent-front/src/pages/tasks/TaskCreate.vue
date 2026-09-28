<template>
  <DashboardLayout>
    <EditPage title="Nouvelle tâche" breadcrumb="Tâches / Création" :saving="saving" :error="error" @submit="submit" @cancel="router.push({ name: 'Tasks' })">
      <TaskForm ref="formRef" v-model="form" />
    </EditPage>
  </DashboardLayout>
</template>

<script setup>
import { reactive, ref } from "vue"
import { useRouter } from "vue-router"
import DashboardLayout from "@/layouts/DashboardLayout.vue"
import EditPage from "@/components/common/EditPage.vue"
import TaskForm from "@/components/task/TaskForm.vue"
import taskService from "@/services/taskService"
import { useAuthStore } from "@/stores/auth"

defineOptions({ name: "TaskCreatePage" })
const router = useRouter()
const auth = useAuthStore()
const formRef = ref(null)
const saving = ref(false)
const error = ref("")
const form = reactive({ title: "", description: "", priority: "medium", dueAt: "", assignedUserId: auth.user?.id ?? null, opportunityId: null, eventId: null })

async function submit() {
  if (!(await formRef.value?.validate())) return
  saving.value = true
  error.value = ""
  try {
    const task = await taskService.create({
      title: form.title.trim(), description: form.description?.trim() || null,
      priority: form.priority, due_at: new Date(form.dueAt).toISOString(),
      assigned_user_id: Number(form.assignedUserId),
      opportunity_id: form.opportunityId ? Number(form.opportunityId) : null,
      event_id: form.eventId ? Number(form.eventId) : null,
    })
    await router.push({ name: "TaskView", params: { id: task.id } })
  } catch (err) { error.value = err.response?.data?.detail ?? "Impossible de créer la tâche" }
  finally { saving.value = false }
}
</script>
