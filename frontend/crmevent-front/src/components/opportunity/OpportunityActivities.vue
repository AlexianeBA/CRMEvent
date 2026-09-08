<template>
  <v-card class="activities-card">
    <div class="activities-header">
      <div>
        <h3>Activités commerciales</h3>
        <p>Notes, appels, emails et réunions</p>
      </div>
      <v-btn v-if="auth.canManageCrm" color="primary" prepend-icon="mdi-plus" @click="openCreate">
        Ajouter une activité
      </v-btn>
    </div>

    <v-alert v-if="error" type="error" variant="tonal" class="ma-5">{{ error }}</v-alert>
    <div v-if="loading" class="state-message">Chargement...</div>
    <div v-else-if="activities.length === 0" class="state-message">Aucune activité commerciale</div>
    <div v-else class="activities-list">
      <div v-for="activity in activities" :key="activity.id" class="activity-row">
        <v-avatar :color="typeColors[activity.type]" variant="tonal" size="42">
          <v-icon :icon="typeIcons[activity.type]" />
        </v-avatar>
        <div class="activity-content">
          <div class="activity-title">
            <strong>{{ typeLabels[activity.type] }}</strong>
            <v-chip :color="statusColors[activity.status]" size="small" variant="tonal">
              {{ statusLabels[activity.status] }}
            </v-chip>
          </div>
          <p>{{ activity.content }}</p>
          <div v-if="activity.scheduled_at" class="scheduled-date">
            <v-icon icon="mdi-calendar-clock" size="small" />
            Prévu le {{ formatDate(activity.scheduled_at) }}
          </div>
          <small>{{ formatDate(activity.updated_at || activity.created_at) }}</small>
        </div>
        <div class="activity-actions">
          <v-btn v-if="auth.canManageCrm && canEdit(activity)" icon="mdi-pencil-outline" size="small" variant="text" title="Modifier" @click="openEdit(activity)" />
          <v-btn v-if="auth.canManageCrm && activity.status === 'draft' && isSchedulable(activity)" size="small" variant="tonal" prepend-icon="mdi-calendar-clock" @click="openSchedule(activity)">Planifier</v-btn>
          <v-btn v-if="auth.canManageCrm && activity.status === 'planned' && isSchedulable(activity)" size="small" variant="text" prepend-icon="mdi-calendar-edit" @click="openSchedule(activity)">Replanifier</v-btn>
          <v-btn v-if="auth.canManageCrm && activity.status === 'draft' && !isSchedulable(activity)" size="small" color="success" variant="tonal" @click="changeStatus(activity, 'done')">Terminer</v-btn>
          <v-btn v-if="auth.canManageCrm && activity.status === 'planned'" size="small" color="success" variant="tonal" @click="changeStatus(activity, 'done')">Terminer</v-btn>
          <v-btn v-if="auth.canManageCrm && canEdit(activity)" icon="mdi-cancel" size="small" color="warning" variant="text" title="Annuler" @click="changeStatus(activity, 'canceled')" />
          <v-btn v-if="auth.canDeleteCrm" icon="mdi-delete-outline" size="small" color="error" variant="text" title="Supprimer" @click="deleteActivity(activity)" />
        </div>
      </div>
    </div>
  </v-card>

  <v-dialog v-model="dialog" max-width="600">
    <v-card :title="editingActivity ? 'Modifier l’activité' : 'Nouvelle activité'">
      <v-card-text>
        <v-alert v-if="dialogError" type="error" variant="tonal" class="mb-4">{{ dialogError }}</v-alert>
        <v-form ref="formRef" @submit.prevent="saveActivity">
          <v-select v-model="form.type" :items="types" item-title="label" item-value="value" label="Type" variant="outlined" :rules="[rules.required]" />
          <v-textarea v-model="form.content" label="Compte rendu ou note" variant="outlined" rows="5" counter="1000" :rules="[rules.required, rules.maxLength]" />
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn variant="text" :disabled="saving" @click="dialog = false">Annuler</v-btn>
        <v-btn color="primary" :loading="saving" @click="saveActivity">Enregistrer</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <v-dialog v-model="scheduleDialog" max-width="500">
    <v-card :title="scheduleActivity?.status === 'planned' ? 'Replanifier l’activité' : 'Planifier l’activité'">
      <v-card-text>
        <v-alert v-if="scheduleError" type="error" variant="tonal" class="mb-4">{{ scheduleError }}</v-alert>
        <p class="mb-4">{{ typeLabels[scheduleActivity?.type] }} — {{ scheduleActivity?.content }}</p>
        <v-text-field
          v-model="scheduledAt"
          label="Date et heure"
          type="datetime-local"
          variant="outlined"
          :min="minimumScheduleDate"
        />
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn variant="text" :disabled="saving" @click="scheduleDialog = false">Annuler</v-btn>
        <v-btn color="primary" :loading="saving" prepend-icon="mdi-calendar-check" @click="schedule">Confirmer</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { onMounted, reactive, ref, watch } from "vue"
import activityService from "@/services/activityService"
import { useAuthStore } from "@/stores/auth"

const props = defineProps({ opportunityId: { type: [Number, String], required: true } })
const emit = defineEmits(["changed"])
const auth = useAuthStore()
const activities = ref([])
const loading = ref(false)
const saving = ref(false)
const error = ref("")
const dialogError = ref("")
const dialog = ref(false)
const scheduleDialog = ref(false)
const scheduleActivity = ref(null)
const scheduledAt = ref("")
const scheduleError = ref("")
const formRef = ref(null)
const editingActivity = ref(null)
const form = reactive({ type: "note", content: "" })

const types = [
  { label: "Note", value: "note" },
  { label: "Appel", value: "call" },
  { label: "Email", value: "email" },
  { label: "Réunion", value: "meeting" },
]
const typeLabels = { note: "Note", call: "Appel", email: "Email", meeting: "Réunion" }
const typeIcons = { note: "mdi-note-text-outline", call: "mdi-phone-outline", email: "mdi-email-outline", meeting: "mdi-account-group-outline" }
const typeColors = { note: "blue-grey", call: "green", email: "blue", meeting: "purple" }
const statusLabels = { draft: "Brouillon", planned: "Planifiée", done: "Terminée", canceled: "Annulée" }
const statusColors = { draft: "grey", planned: "blue", done: "success", canceled: "warning" }
const rules = {
  required: (value) => Boolean(String(value ?? "").trim()) || "Ce champ est obligatoire",
  maxLength: (value) => String(value ?? "").length <= 1000 || "1000 caractères maximum",
}
const minimumScheduleDate = new Date(Date.now() + 60_000).toISOString().slice(0, 16)

async function loadActivities() {
  if (!props.opportunityId) return
  loading.value = true
  error.value = ""
  try {
    activities.value = await activityService.getByOpportunity(props.opportunityId)
  } catch (err) {
    error.value = err.response?.data?.detail ?? "Impossible de charger les activités"
  } finally {
    loading.value = false
  }
}

function openCreate() {
  editingActivity.value = null
  Object.assign(form, { type: "note", content: "" })
  dialogError.value = ""
  dialog.value = true
}

function openEdit(activity) {
  editingActivity.value = activity
  Object.assign(form, { type: activity.type, content: activity.content })
  dialogError.value = ""
  dialog.value = true
}

async function saveActivity() {
  const validation = await formRef.value?.validate()
  if (!validation?.valid) return
  saving.value = true
  dialogError.value = ""
  try {
    const payload = { type: form.type, content: form.content.trim() }
    if (editingActivity.value) {
      await activityService.update(editingActivity.value.id, payload)
    } else {
      await activityService.create({ ...payload, opportunity_id: Number(props.opportunityId) })
    }
    dialog.value = false
    await loadActivities()
    emit("changed")
  } catch (err) {
    dialogError.value = err.response?.data?.detail ?? "Impossible d'enregistrer l'activité"
  } finally {
    saving.value = false
  }
}

async function changeStatus(activity, status) {
  error.value = ""
  try {
    await activityService.updateStatus(activity.id, status)
    await loadActivities()
    emit("changed")
  } catch (err) {
    error.value = err.response?.data?.detail ?? "Impossible de modifier le statut"
  }
}

function openSchedule(activity) {
  scheduleActivity.value = activity
  scheduledAt.value = activity.scheduled_at
    ? new Date(activity.scheduled_at).toISOString().slice(0, 16)
    : ""
  scheduleError.value = ""
  scheduleDialog.value = true
}

async function schedule() {
  if (!scheduledAt.value) {
    scheduleError.value = "Sélectionnez une date et une heure"
    return
  }
  if (new Date(scheduledAt.value) <= new Date()) {
    scheduleError.value = "La date de planification doit être dans le futur"
    return
  }

  saving.value = true
  scheduleError.value = ""
  try {
    if (scheduleActivity.value.status === "planned") {
      await activityService.update(scheduleActivity.value.id, {
        scheduled_at: new Date(scheduledAt.value).toISOString(),
      })
    } else {
      await activityService.updateStatus(
        scheduleActivity.value.id,
        "planned",
        new Date(scheduledAt.value).toISOString(),
      )
    }
    scheduleDialog.value = false
    await loadActivities()
    emit("changed")
  } catch (err) {
    scheduleError.value = err.response?.data?.detail ?? "Impossible de planifier l'activité"
  } finally {
    saving.value = false
  }
}

async function deleteActivity(activity) {
  if (!window.confirm(`Supprimer cette ${typeLabels[activity.type].toLowerCase()} ?`)) return
  try {
    await activityService.delete(activity.id)
    await loadActivities()
    emit("changed")
  } catch (err) {
    error.value = err.response?.data?.detail ?? "Impossible de supprimer l'activité"
  }
}

const canEdit = (activity) => ["draft", "planned"].includes(activity.status)
const isSchedulable = (activity) => ["call", "meeting"].includes(activity.type)
const formatDate = (value) => new Intl.DateTimeFormat("fr-FR", { dateStyle: "medium", timeStyle: "short" }).format(new Date(value))

watch(() => props.opportunityId, loadActivities)
onMounted(loadActivities)
</script>

<style scoped>
.activities-card { margin-top: 24px; }
.activities-header { display: flex; justify-content: space-between; align-items: center; gap: 20px; padding: 20px 24px; border-bottom: 1px solid #eee; }
.activities-header h3, .activities-header p { margin: 0; }
.activities-header p { margin-top: 4px; color: #6b7280; }
.activities-list { padding: 0 24px; }
.activity-row { display: flex; align-items: flex-start; gap: 14px; padding: 18px 0; border-bottom: 1px solid #eee; }
.activity-row:last-child { border-bottom: 0; }
.activity-content { flex: 1; min-width: 0; }
.activity-title { display: flex; align-items: center; gap: 10px; }
.activity-content p { margin: 7px 0; white-space: pre-wrap; }
.activity-content small { color: #6b7280; }
.scheduled-date { display: flex; align-items: center; gap: 6px; margin: 8px 0; color: #1d4ed8; font-weight: 600; }
.activity-actions { display: flex; align-items: center; justify-content: flex-end; gap: 4px; flex-wrap: wrap; }
.state-message { padding: 36px; text-align: center; color: #6b7280; }
@media (max-width: 800px) { .activities-header, .activity-row { align-items: stretch; flex-direction: column; } .activity-actions { justify-content: flex-start; } }
</style>
