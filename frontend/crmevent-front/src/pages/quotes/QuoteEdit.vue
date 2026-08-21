<template>
  <DashboardLayout>
    <div v-if="loading" class="loading-container">
      <v-progress-circular indeterminate color="primary" size="48" />
      <p>Chargement du devis...</p>
    </div>
    <EditPage v-else title="Modifier le devis" breadcrumb="Devis / Modification" :saving="saving" :error="error" @submit="submit" @cancel="goBack">
      <QuoteForm ref="quoteFormRef" v-model="form" editing />
    </EditPage>
  </DashboardLayout>
</template>

<script setup>
import { onMounted, ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import DashboardLayout from "@/layouts/DashboardLayout.vue"
import EditPage from "@/components/common/EditPage.vue"
import QuoteForm from "@/components/quotes/QuoteForm.vue"
import quoteService from "@/services/quotesService"

const route = useRoute()
const router = useRouter()
const quoteFormRef = ref(null)
const loading = ref(false)
const saving = ref(false)
const error = ref("")
const form = ref({ title: "", totalAmount: null, companyId: null, opportunityId: null, assignedUserId: null, eventId: null })

async function loadQuote() {
  loading.value = true
  error.value = ""
  try {
    const quote = await quoteService.getById(route.params.id)
    Object.assign(form.value, {
      title: quote.title ?? "",
      totalAmount: Number(quote.total_amount),
      companyId: quote.company_id,
      opportunityId: quote.opportunity_id,
      assignedUserId: quote.assigned_user_id,
      eventId: quote.event_id,
    })
  } catch (err) {
    error.value = err.response?.data?.detail ?? "Impossible de charger le devis"
  } finally {
    loading.value = false
  }
}

async function submit() {
  error.value = ""
  if (!(await quoteFormRef.value?.validate())) {
    error.value = "Merci de corriger les champs du formulaire"
    return
  }
  saving.value = true
  try {
    const quote = await quoteService.update(route.params.id, {
      title: form.value.title.trim(),
      total_amount: Number(form.value.totalAmount),
    })
    await router.push({ name: "QuoteView", params: { id: quote.id } })
  } catch (err) {
    console.error("Erreur pendant la modification du devis :", err)
    error.value = err.response?.data?.detail ?? "Impossible de modifier le devis"
  } finally {
    saving.value = false
  }
}

function goBack() { router.push({ name: "QuoteView", params: { id: route.params.id } }) }
onMounted(loadQuote)
</script>

<style scoped>
.loading-container { display: flex; min-height: 400px; align-items: center; justify-content: center; flex-direction: column; gap: 16px; }
.loading-container p { margin: 0; color: #6b7280; }
</style>
