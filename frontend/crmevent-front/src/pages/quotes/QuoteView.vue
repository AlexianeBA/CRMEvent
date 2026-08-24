<template>
  <DashboardLayout>
    <DetailPage
      :title="quote?.number || 'Devis'"
      :subtitle="quote?.title"
      breadcrumb="Devis / Détail"
      :loading="loading"
      :error="error"
      :show-edit="canEdit"
      @back="goToList"
      @edit="goToEdit"
    >
      <template #actions>
        <v-btn v-if="quote?.status === 'draft'" color="primary" prepend-icon="mdi-send-outline" :loading="actionLoading" @click="changeStatus('sent')">Envoyer</v-btn>
        <v-btn v-if="quote?.status === 'sent'" color="success" prepend-icon="mdi-check-circle-outline" :loading="actionLoading" @click="acceptQuote">Accepter</v-btn>
        <v-btn v-if="quote?.status === 'sent'" color="error" variant="tonal" prepend-icon="mdi-close-circle-outline" :loading="actionLoading" @click="changeStatus('rejected')">Refuser</v-btn>
        <v-btn v-if="quote?.status === 'sent'" color="warning" variant="tonal" prepend-icon="mdi-clock-alert-outline" :loading="actionLoading" @click="changeStatus('expired')">Expirer</v-btn>
        <v-btn v-if="canLock" variant="tonal" prepend-icon="mdi-lock-outline" :loading="actionLoading" @click="changeStatus('locked')">Verrouiller</v-btn>
        <v-btn v-if="quote?.status === 'draft'" color="error" variant="tonal" prepend-icon="mdi-delete-outline" :loading="actionLoading" @click="deleteQuote">Supprimer</v-btn>
      </template>

      <QuoteDetails v-if="quote" :quote="quote" />
    </DetailPage>
  </DashboardLayout>
</template>

<script setup>
import { computed, onMounted, ref, watch } from "vue"
import { useRoute, useRouter } from "vue-router"
import DashboardLayout from "@/layouts/DashboardLayout.vue"
import DetailPage from "@/components/common/DetailPage.vue"
import QuoteDetails from "@/components/quotes/QuoteDetails.vue"
import quoteService from "@/services/quotesService"

const route = useRoute()
const router = useRouter()
const quote = ref(null)
const loading = ref(false)
const actionLoading = ref(false)
const error = ref("")

const canEdit = computed(() => ["draft", "sent"].includes(quote.value?.status))
const canLock = computed(() => ["accepted", "rejected", "expired"].includes(quote.value?.status))

async function loadQuote() {
  loading.value = true
  error.value = ""
  try {
    quote.value = await quoteService.getById(route.params.id)
  } catch (err) {
    error.value = err.response?.data?.detail ?? "Impossible de charger le devis"
  } finally {
    loading.value = false
  }
}

async function runAction(action) {
  actionLoading.value = true
  error.value = ""
  try {
    await action()
  } catch (err) {
    console.error("Erreur pendant l'action sur le devis :", err)
    error.value = err.response?.data?.detail ?? "Impossible d'effectuer cette action"
  } finally {
    actionLoading.value = false
  }
}

function changeStatus(status) {
  return runAction(async () => {
    quote.value = await quoteService.updateStatus(route.params.id, status)
  })
}

function acceptQuote() {
  return runAction(async () => {
    const result = await quoteService.accept(route.params.id)
    quote.value = result.quote
    await router.push({ name: "InvoiceView", params: { id: result.invoice.id } })
  })
}

async function deleteQuote() {
  if (!window.confirm(`Supprimer le devis ${quote.value.number} ?`)) return
  await runAction(async () => {
    await quoteService.delete(route.params.id)
    await router.push({ name: "Quotes" })
  })
}

function goToList() { router.push({ name: "Quotes" }) }
function goToEdit() { router.push({ name: "QuoteEdit", params: { id: route.params.id } }) }

watch(() => route.params.id, (newId, oldId) => { if (newId && newId !== oldId) loadQuote() })
onMounted(loadQuote)
</script>
