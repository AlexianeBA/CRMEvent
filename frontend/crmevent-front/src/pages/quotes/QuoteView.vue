<template>
  <DetailPage
    :title="quote?.number || 'Devis'"
    :subtitle="quote?.title"
    breadcrumb="Devis / Détail"
    :loading="loading"
    :error="error"
    :show-edit="canEdit"
    @back="router.push('/quotes')"
    @edit="goToEdit"
  >
    <template #actions>
      <v-btn
        v-if="quote?.status === 'draft'"
        color="primary"
        prepend-icon="mdi-send-outline"
        @click="sendQuote"
      >
        Envoyer
      </v-btn>

      <v-btn
        v-if="quote?.status === 'sent'"
        color="success"
        prepend-icon="mdi-check-circle-outline"
        @click="acceptQuote"
      >
        Accepter
      </v-btn>
    </template>

    <div v-if="quote" class="details-grid">
      <DetailsCard
        title="Informations du devis"
        icon="mdi-file-document-outline"
        :item="quote"
        :fields="quoteFields"
      >
        <template #field-status="{ value }">
          <v-chip
            :color="getStatusColor(value)"
            variant="tonal"
            size="small"
          >
            {{ getStatusLabel(value) }}
          </v-chip>
        </template>
      </DetailsCard>

      <DetailsCard
        title="Relations"
        icon="mdi-link-variant"
        :item="quote"
        :fields="relationFields"
      />
    </div>
  </DetailPage>
</template>

<script setup>
import { computed, onMounted, ref } from "vue"
import { useRoute, useRouter } from "vue-router"

import DetailPage from "@/components/common/DetailPage.vue"
import DetailsCard from "@/components/common/DetailsCard.vue"
import { quoteService } from "@/services/quoteService"

const route = useRoute()
const router = useRouter()

const quote = ref(null)
const loading = ref(false)
const error = ref("")

const canEdit = computed(() =>
  ["draft", "sent"].includes(quote.value?.status),
)

const quoteFields = [
  { key: "number", label: "Numéro" },
  { key: "title", label: "Titre" },
  {
    key: "total_amount",
    label: "Montant",
    formatter: (value) =>
      new Intl.NumberFormat("fr-FR", {
        style: "currency",
        currency: "EUR",
      }).format(Number(value ?? 0)),
  },
  { key: "status", label: "Statut" },
]

const relationFields = [
  { key: "company_id", label: "Entreprise" },
  { key: "opportunity_id", label: "Opportunité" },
  { key: "event_id", label: "Événement" },
  { key: "assigned_user_id", label: "Utilisateur assigné" },
]

async function loadQuote() {
  loading.value = true
  error.value = ""

  try {
    quote.value = await quoteService.getById(route.params.id)
  } catch (err) {
    error.value =
      err.response?.data?.detail ??
      "Impossible de charger le devis"
  } finally {
    loading.value = false
  }
}

function goToEdit() {
  router.push({
    name: "QuoteEdit",
    params: {
      id: route.params.id,
    },
  })
}

async function sendQuote() {
  quote.value = await quoteService.updateStatus(
    route.params.id,
    "sent",
  )
}

async function acceptQuote() {
  quote.value = await quoteService.accept(route.params.id)
}

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

onMounted(loadQuote)
</script>

<style scoped>
.details-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 24px;
}

@media (max-width: 850px) {
  .details-grid {
    grid-template-columns: 1fr;
  }
}
</style>