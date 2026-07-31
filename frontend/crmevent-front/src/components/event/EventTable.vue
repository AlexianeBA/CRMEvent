<template>
  <DataTable
    :items="store.events"
    :columns="columns"
    :search-fields="['title', 'type', 'date', 'duration', 'location']"
    :loading="store.loading"
  />
</template>

<script setup>
import { onMounted } from "vue"
import { useEventStore } from "@/stores/event"
import DataTable from "@/components/DataTable.vue"

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

onMounted(() => {
  store.loadEvents()
})
</script>