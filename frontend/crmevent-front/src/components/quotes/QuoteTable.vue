<template>
  <DataTable
    :items="store.quotes"
    :columns="columns"
    :search-fields="['number', 'title', 'status']"
    :loading="store.loading"
  >
    <template #cell-status="{ value }">
      <v-chip
        :color="getStatusColor(value)"
        size="small"
        variant="tonal"
      >
        {{ getStatusLabel(value) }}
      </v-chip>
    </template>
  </DataTable>
</template>

<script setup>
import { onMounted } from "vue"
import { useQuoteStore } from "@/stores/quotes"
import DataTable from "@/components/DataTable.vue"

const store = useQuoteStore()

const columns = [
  {
    key: "number",
    label: "Numéro",
  },
  {
    key: "title",
    label: "Titre",
  },
  {
    key: "total_amount",
    label: "Total",
    formatter: (value) =>
      new Intl.NumberFormat("fr-FR", {
        style: "currency",
        currency: "EUR",
      }).format(Number(value ?? 0)),
  },
  {
    key: "status",
    label: "Statut",
  },
]

function getStatusLabel(status) {
  const labels = {
    draft: "Brouillon",
    sent: "Envoyé",
    accepted: "Accepté",
    rejected: "Refusé",
    expired: "Expiré",
    locked: "Verrouillé",
  }

  return labels[status] ?? status
}

function getStatusColor(status) {
  const colors = {
    draft: "grey",
    sent: "blue",
    accepted: "green",
    rejected: "red",
    expired: "orange",
    locked: "purple",
  }

  return colors[status] ?? "grey"
}

onMounted(() => {
  store.loadQuotes()
})
</script>