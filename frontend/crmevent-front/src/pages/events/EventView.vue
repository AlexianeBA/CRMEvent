<template>
  <DashboardLayout>
    <DetailPage
      :title="event?.firstName || 'Détail de l\'événement'"
      breadcrumb="Événements / Détail"
      :loading="loading"
      :error="error"
      @back="goToList"
      @edit="goToEdit"
    >
      <EventDetails
        v-if="event"
        :event="event"
      />
    </DetailPage>
  </DashboardLayout>
</template>

<script setup>
import { onMounted, ref, watch } from "vue"
import { useRoute, useRouter } from "vue-router"

import DashboardLayout from "@/layouts/DashboardLayout.vue"
import DetailPage from "@/components/common/DetailPage.vue"
import EventDetails from "@/components/event/EventDetails.vue"
import { eventService } from "@/services/eventService"

const route = useRoute()
const router = useRouter()

const event = ref(null)
const loading = ref(false)
const error = ref("")

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