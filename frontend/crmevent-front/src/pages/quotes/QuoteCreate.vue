<template>
  <DashboardLayout>
    <EditPage title="Nouveau devis" breadcrumb="Devis / Création" :saving="saving" :error="error" @submit="submit" @cancel="goBack">
      <QuoteForm ref="quoteFormRef" v-model="form" />
    </EditPage>
  </DashboardLayout>
</template>

<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import DashboardLayout from "@/layouts/DashboardLayout.vue"
import EditPage from "@/components/common/EditPage.vue"
import QuoteForm from "@/components/quotes/QuoteForm.vue"
import quoteService from "@/services/quotesService"

const router = useRouter()
const quoteFormRef = ref(null)
const saving = ref(false)
const error = ref("")
const form = ref({ title: "", companyId: null, opportunityId: null, assignedUserId: null, eventId: null, lines: [{ description: "", quantity: 1, unit: "unité", unitPrice: 0, discountRate: 0, vatRate: 20 }] })

async function submit() {
  error.value = ""
  if (!(await quoteFormRef.value?.validate())) {
    error.value = "Merci de corriger les champs du formulaire"
    return
  }
  saving.value = true
  try {
    const quote = await quoteService.create({
      title: form.value.title.trim(),
      lines: form.value.lines.map((line, position) => ({ description: line.description.trim(), quantity: Number(line.quantity), unit: line.unit.trim(), unit_price_excl_tax: Number(line.unitPrice), discount_rate: Number(line.discountRate), vat_rate: Number(line.vatRate), position })),
      company_id: Number(form.value.companyId),
      opportunity_id: Number(form.value.opportunityId),
      assigned_user_id: Number(form.value.assignedUserId),
      event_id: form.value.eventId ? Number(form.value.eventId) : null,
    })
    await router.push({ name: "QuoteView", params: { id: quote.id } })
  } catch (err) {
    console.error("Erreur pendant la création du devis :", err)
    error.value = err.response?.data?.detail ?? "Impossible de créer le devis"
  } finally {
    saving.value = false
  }
}

function goBack() { router.push({ name: "Quotes" }) }
</script>
