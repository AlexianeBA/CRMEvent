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
      <template #actions="{ item }">
      <div class="action-buttons">
        <v-btn
          icon="mdi-eye-outline"
          variant="text"
          size="small"
          @click="viewQuote(item)"
        />

        <v-btn
          icon="mdi-pencil-outline"
          variant="text"
          size="small"
          @click="editQuote(item)"
        />

        <v-btn
          icon="mdi-delete-outline"
          variant="text"
          size="small"
          color="error"
          @click="deleteQuote(item)"
        />
      </div>
    </template>
  </DataTable>
</template>

<script setup>
import { onMounted } from "vue"
import { useRouter } from "vue-router"
import { useQuoteStore } from "@/stores/quotes"
import DataTable from "@/components/common/DataTable.vue"

const router = useRouter()
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
function viewQuote(quote) {
  router.push(`/quotes/${quote.id}`)
}

function editQuote(quote) {
  router.push(`/quotes/${quote.id}/edit`)
}

async function deleteQuote(quote) {
  const confirmed = window.confirm(
    `Supprimer le devis ${quote.number} ?`,
  )

  if (!confirmed) {
    return
  }

  await store.deleteQuote(quote.id)
}

onMounted(() => {
  store.loadQuotes()
})
</script>