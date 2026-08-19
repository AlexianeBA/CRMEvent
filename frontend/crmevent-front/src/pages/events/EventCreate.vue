<template>
  <DashboardLayout>
    <EditPage
      title="Nouvel événement"
      breadcrumb="Événements / Création"
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
import { ref } from "vue"
import { useRouter } from "vue-router"

import DashboardLayout from "@/layouts/DashboardLayout.vue"
import EditPage from "@/components/common/EditPage.vue"
import EventForm from "@/components/event/EventForm.vue"
import { eventService } from "@/services/eventService"

const router = useRouter()

const eventFormRef = ref(null)

const saving = ref(false)
const error = ref("")

const form = ref({
  title: "",
  type: "",
  date: "",
  duration: null,
  location: "",
  description: "",
  status: "draft",
  companyId: null,
  opportunityId: null,
  assignedUserId: null,
  contactId: null,
})

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
    const createdEvent =
        await eventService.create(buildPayload())

    await router.push({
        name: "EventView",
        params: {
            id: createdEvent.id,
        },
        })

    router.push({
      name: "Events",
    })
  } catch (err) {
    console.error(
      "Erreur pendant la création de l'événement :",
      err,
    )

    error.value =
      err.response?.data?.detail ??
      "Impossible de créer l'événement"
  } finally {
    saving.value = false
  }
}

function buildPayload() {
  return {
    title: form.value.title.trim(),
    type: form.value.type,
    date: toApiDate(form.value.date),
    duration: Number(form.value.duration),
    location: form.value.location.trim(),
    description: normalizeOptionalValue(
      form.value.description,
    ),
    status: form.value.status,
    company_id: Number(
      form.value.companyId,
    ),
    opportunity_id: Number(
      form.value.opportunityId,
    ),
    assigned_user_id: Number(
      form.value.assignedUserId,
    ),
    contact_id: normalizeOptionalId(
      form.value.contactId,
    ),
  }
}

function toApiDate(value) {
  if (!value) {
    return ""
  }

  const [year, month, day] = value.split("-")

  return `${day}-${month}-${year}`
}

function normalizeOptionalValue(value) {
  const normalized = String(value ?? "").trim()

  return normalized || null
}

function normalizeOptionalId(value) {
  if (
    value === null ||
    value === undefined ||
    value === ""
  ) {
    return null
  }

  return Number(value)
}



function goBack() {
  router.push({
    name: "Events",
  })
}
</script>
