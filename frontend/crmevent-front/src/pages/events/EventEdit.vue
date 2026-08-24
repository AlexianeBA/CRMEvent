<template>
  <DashboardLayout>
    <div
      v-if="loading"
      class="loading-container"
    >
      <v-progress-circular
        indeterminate
        color="primary"
        size="48"
      />

      <p>Chargement de l'événement...</p>
    </div>

    <EditPage
      v-else
      title="Modifier l'événement"
      breadcrumb="Événements / Modification"
      :saving="saving"
      :error="error"
      @submit="submit"
      @cancel="goBack"
    >
      <EventForm
        ref="eventFormRef"
        v-model="form"
      />
    </EditPage>
  </DashboardLayout>
</template>

<script setup>
import { onMounted, ref } from "vue"
import { useRoute, useRouter } from "vue-router"

import DashboardLayout from "@/layouts/DashboardLayout.vue"
import EditPage from "@/components/common/EditPage.vue"
import EventForm from "@/components/event/EventForm.vue"
import { eventService } from "@/services/eventService"

const route = useRoute()
const router = useRouter()

const eventFormRef = ref(null)

const loading = ref(false)
const saving = ref(false)
const error = ref("")

const form = ref({
  title: "",
  date: "",
  type: "",
  duration: null,
  location: "",
  description: "",
  companyId: null,
  opportunityId: null,
  assignedUserId: null,
  contactId: null,
})

async function loadEvent() {
  const eventId = route.params.id

  if (!eventId) {
    error.value = "L'identifiant de l'événement est manquant"
    return
  }

  loading.value = true
  error.value = ""

  try {
    const event = await eventService.getById(eventId)

    Object.assign(form.value, {
      title: event.title ?? "",
      date: toInputDate(event.date),
      type: event.type ?? "",
      duration: event.duration ?? null,
      location: event.location ?? "",
      description: event.description ?? "",
      companyId: event.company_id ?? null,
      opportunityId: event.opportunity_id ?? null,
      assignedUserId:
        event.assigned_user_id ?? null,
      contactId: event.contact_id ?? null,
    })
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

async function submit() {
  error.value = ""

  const isValid =
    await eventFormRef.value?.validate()

  if (!isValid) {
    error.value =
      "Merci de corriger les champs du formulaire"
    return
  }

  saving.value = true

  try {
    const updatedEvent =
      await eventService.update(
        route.params.id,
        buildPayload(),
      )

    router.push({
      name: "EventView",
      params: {
        id: updatedEvent?.id ?? route.params.id,
      },
    })
  } catch (err) {
    console.error(
      "Erreur pendant la modification de l'événement :",
      err,
    )

    error.value =
      err.response?.data?.detail ??
      "Impossible de modifier l'événement"
  } finally {
    saving.value = false
  }
}

function buildPayload() {
  return {
    title: form.value.title.trim(),
    date: toApiDate(form.value.date),
    type: form.value.type,
    duration: Number(form.value.duration),
    location: form.value.location.trim(),
    description: normalizeOptionalValue(
      form.value.description,
    ),
    company_id: Number(form.value.companyId),
    opportunity_id: Number(form.value.opportunityId),
    assigned_user_id: Number(form.value.assignedUserId),
    contact_id: normalizeOptionalId(form.value.contactId),
  }
}

function toApiDate(value) {
  if (!value) {
    return ""
  }

  const [year, month, day] = value.split("-")

  return `${day}-${month}-${year}`
}

function toInputDate(value) {
  if (!value) {
    return ""
  }

  const parts = value.split("-")

  if (
    parts.length === 3 &&
    parts[0].length === 2
  ) {
    const [day, month, year] = parts

    return `${year}-${month}-${day}`
  }

  return value
}

function normalizeOptionalId(value) {
  if (value === null || value === undefined || value === "") {
    return null
  }

  return Number(value)
}

function normalizeOptionalValue(value) {
  const normalized = String(value ?? "").trim()

  return normalized || null
}

function goBack() {
  router.push({
    name: "EventView",
    params: {
      id: route.params.id,
    },
  })
}

onMounted(loadEvent)
</script>

<style scoped>
.loading-container {
  display: flex;
  min-height: 400px;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  gap: 16px;
}

.loading-container p {
  margin: 0;
  color: #6b7280;
}
</style>
