<template>
  <DataTable ref="table" resource="events" :columns="columns">
    <template #actions="{ item }">
      <div class="action-buttons">
        <v-btn icon="mdi-eye-outline" variant="text" size="small" @click="viewEvent(item)" />

        <v-btn
          v-if="auth.canManageCrm && ['draft', 'scheduled'].includes(item.status)"
          icon="mdi-pencil-outline"
          variant="text"
          size="small"
          @click="editEvent(item)"
        />

        <v-btn
          v-if="auth.canDeleteCrm && ['draft', 'canceled'].includes(item.status)"
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
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import eventService from '@/services/eventService'
import DataTable from '@/components/common/DataTable.vue'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const table = ref(null)
const auth = useAuthStore()

const typeLabels = {
  webinar: 'Webinaire',
  workshop: 'Atelier',
  conference: 'Conférence',
}

const statusLabels = {
  draft: 'Brouillon',
  scheduled: 'Planifié',
  held: 'Réalisé',
  canceled: 'Annulé',
  locked: 'Clôturé',
}

const columns = [
  {
    key: 'title',
    label: 'Titre',
  },
  {
    key: 'type',
    label: 'Type',
    formatter: (value) => typeLabels[value] ?? value,
  },
  {
    key: 'date',
    label: 'Date',
  },
  {
    key: 'duration',
    label: 'Durée',
    formatter: (value) => `${value} h`,
  },
  {
    key: 'location',
    label: 'Localisation',
  },
  {
    key: 'status',
    label: 'Statut',
    formatter: (value) => statusLabels[value] ?? value,
  },
]
function viewEvent(event) {
  router.push(`/events/${event.id}`)
}
function editEvent(event) {
  router.push(`/events/${event.id}/edit`)
}
async function deleteEvent(event) {
  const confirmed = window.confirm(`Supprimer l'événement ${event.title} ?`)

  if (!confirmed) {
    return
  }

  await eventService.delete(event.id)
  table.value?.reload()
}
</script>
