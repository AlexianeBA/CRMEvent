<template>
  <DashboardLayout>
    <DetailPage
      :title="event?.title || 'Détail de l\'événement'"
      :subtitle="statusLabels[event?.status]"
      breadcrumb="Événements / Détail"
      :loading="loading"
      :error="error"
      :show-edit="canEdit"
      @back="goToList"
      @edit="goToEdit"
    >
      <template #actions>
        <v-btn
          v-for="transition in transitions"
          :key="transition.status"
          :color="transition.color"
          :variant="transition.variant"
          :prepend-icon="transition.icon"
          :loading="actionLoading"
          @click="changeStatus(transition.status)"
        >
          {{ transition.label }}
        </v-btn>

        <v-btn
          v-if="canDelete"
          color="error"
          variant="tonal"
          prepend-icon="mdi-delete-outline"
          :loading="actionLoading"
          @click="deleteEvent"
        >
          Supprimer
        </v-btn>
      </template>

      <div v-if="event" class="workflow">
        <div
          v-for="step in workflowSteps"
          :key="step.status"
          class="workflow-step"
          :class="{
            active: event.status === step.status,
            completed: completedStatuses.includes(step.status),
          }"
        >
          <v-icon :icon="step.icon" size="20" />
          <span>{{ step.label }}</span>
        </div>
      </div>

      <v-alert
        v-if="event?.status === 'canceled'"
        type="warning"
        variant="tonal"
        class="mb-6"
      >
        Cet événement a été annulé. Vous pouvez le clôturer ou le supprimer.
      </v-alert>

      <EventDetails
        v-if="event"
        :event="event"
      />
    </DetailPage>
  </DashboardLayout>
</template>

<script setup>
import { computed, onMounted, ref, watch } from "vue"
import { useRoute, useRouter } from "vue-router"

import DashboardLayout from "@/layouts/DashboardLayout.vue"
import DetailPage from "@/components/common/DetailPage.vue"
import EventDetails from "@/components/event/EventDetails.vue"
import { eventService } from "@/services/eventService"

const route = useRoute()
const router = useRouter()

const event = ref(null)
const loading = ref(false)
const actionLoading = ref(false)
const error = ref("")

const statusLabels = {
  draft: "Brouillon",
  scheduled: "Planifié",
  held: "Réalisé",
  canceled: "Annulé",
  locked: "Clôturé",
}

const transitionMap = {
  draft: [
    { status: "scheduled", label: "Planifier", color: "primary", variant: "flat", icon: "mdi-calendar-check" },
    { status: "canceled", label: "Annuler", color: "error", variant: "tonal", icon: "mdi-calendar-remove" },
  ],
  scheduled: [
    { status: "held", label: "Marquer réalisé", color: "success", variant: "flat", icon: "mdi-check-circle-outline" },
    { status: "canceled", label: "Annuler", color: "error", variant: "tonal", icon: "mdi-calendar-remove" },
  ],
  held: [
    { status: "locked", label: "Clôturer", color: "primary", variant: "flat", icon: "mdi-lock-outline" },
  ],
  canceled: [
    { status: "locked", label: "Clôturer", color: "primary", variant: "tonal", icon: "mdi-lock-outline" },
  ],
}

const workflowSteps = [
  { status: "draft", label: "Préparation", icon: "mdi-file-edit-outline" },
  { status: "scheduled", label: "Planification", icon: "mdi-calendar-clock" },
  { status: "held", label: "Réalisation", icon: "mdi-calendar-check" },
  { status: "locked", label: "Clôture", icon: "mdi-lock-outline" },
]

const workflowOrder = workflowSteps.map((step) => step.status)
const transitions = computed(() => transitionMap[event.value?.status] ?? [])
const canEdit = computed(() => ["draft", "scheduled"].includes(event.value?.status))
const canDelete = computed(() => ["draft", "canceled"].includes(event.value?.status))
const completedStatuses = computed(() => {
  const currentIndex = workflowOrder.indexOf(event.value?.status)
  return currentIndex < 0 ? [] : workflowOrder.slice(0, currentIndex)
})

async function loadEvent() {
  const eventId = route.params.id

  if (!eventId) {
    error.value = "L'identifiant de l'événement est manquant"
    return
  }

  loading.value = true
  error.value = ""
  event.value = null

  try {
    event.value = await eventService.getById(eventId)
  } catch (err) {
    console.error(
      "Erreur pendant le chargement de l'événement :",
      err,
    )

    error.value =
      err.response?.data?.detail ??
      "Impossible de charger l'événement"
  } finally {
    loading.value = false
  }
}

function goToList() {
  router.push({
    name: "Events",
  })
}

function goToEdit() {
  router.push({
    name: "EventEdit",
    params: {
      id: route.params.id,
    },
  })
}

async function runAction(action) {
  actionLoading.value = true
  error.value = ""

  try {
    await action()
  } catch (err) {
    console.error("Erreur pendant l'action sur l'événement :", err)
    error.value = err.response?.data?.detail ?? "Impossible d'effectuer cette action"
  } finally {
    actionLoading.value = false
  }
}

function changeStatus(status) {
  return runAction(async () => {
    event.value = await eventService.updateStatus(route.params.id, status)
  })
}

async function deleteEvent() {
  if (!window.confirm(`Supprimer l'événement ${event.value.title} ?`)) return

  await runAction(async () => {
    await eventService.delete(route.params.id)
    await router.push({ name: "Events" })
  })
}

watch(
  () => route.params.id,
  (newId, oldId) => {
    if (newId && newId !== oldId) {
      loadEvent()
    }
  },
)

onMounted(loadEvent)
</script>

<style scoped>
.workflow {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 10px;
  margin-bottom: 24px;
}

.workflow-step {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px;
  color: #6b7280;
  background: #f3f4f6;
  border-radius: 10px;
}

.workflow-step.completed {
  color: #047857;
  background: #d1fae5;
}

.workflow-step.active {
  color: #1d4ed8;
  background: #dbeafe;
  font-weight: 700;
}

@media (max-width: 750px) {
  .workflow {
    grid-template-columns: 1fr 1fr;
  }
}
</style>
