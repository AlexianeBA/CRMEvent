<template>
  <DataTable
    :items="store.events"
    :columns="columns"
    :search-fields="['title', 'type', 'date', 'duration', 'location']"
    :loading="store.loading"
  >
  <template #actions="{ item }">
      <div class="action-buttons">
        <v-btn
          icon="mdi-eye-outline"
          variant="text"
          size="small"
          @click="viewEvent(item)"
        />

        <v-btn
          icon="mdi-pencil-outline"
          variant="text"
          size="small"
          @click="editEvent(item)"
        />

        <v-btn
          icon="mdi-delete-outline"
          variant="text"
          size="small"
          color="error"
          @click="deleteEvent(item)"
        />
      </div>
    </template>
  </DataTable>
</template>

<script setup>
import { onMounted } from "vue"
import { useRouter } from "vue-router"
import { useEventStore } from "@/stores/event"
import DataTable from "@/components/common/DataTable.vue"

const router = useRouter()
const store = useEventStore()

const columns = [
  {
    key: "title",
    label: "Titre",
  },
  {
    key: "type",
    label: "Type",
  },
  {
    key: "date",
    label: "Date",
  },
  {
    key: "duration",
    label: "Durée",
  },
  {
    key: "location",
    label: "Localisation",
  },
]
function viewEvent(event) {
  router.push(`/events/${event.id}`)
}
function editEvent(event) {
  router.push(`/events/${event.id}/edit`)
}
async function deleteEvent(event) {
  const confirmed = window.confirm(
    `Supprimer l'événement ${event.title} ?`,
  )

  if (!confirmed) {
    return
  }

  await store.deleteEvent(event.id)
}

onMounted(() => {
  store.loadEvents()
})
</script>