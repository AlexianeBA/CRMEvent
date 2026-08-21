<template>
  <DashboardLayout>
    <div v-if="loading" class="loading-container"><v-progress-circular indeterminate color="primary" size="48" /><p>Chargement de la facture...</p></div>
    <EditPage v-else title="Modifier la facture" breadcrumb="Factures / Modification" :saving="saving" :error="error" @submit="submit" @cancel="goBack">
      <InvoiceForm ref="invoiceFormRef" v-model="form" />
    </EditPage>
  </DashboardLayout>
</template>

<script setup>
import { onMounted, ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import DashboardLayout from "@/layouts/DashboardLayout.vue"
import EditPage from "@/components/common/EditPage.vue"
import InvoiceForm from "@/components/invoice/InvoiceForm.vue"
import invoiceService from "@/services/invoiceService"

const route = useRoute()
const router = useRouter()
const invoiceFormRef = ref(null)
const loading = ref(false)
const saving = ref(false)
const error = ref("")
const form = ref({ title: "", totalAmount: null })

async function loadInvoice() {
  loading.value = true
  try {
    const invoice = await invoiceService.getById(route.params.id)
    form.value.title = invoice.title ?? ""
    form.value.totalAmount = Number(invoice.total_amount)
  } catch (err) {
    error.value = err.response?.data?.detail ?? "Impossible de charger la facture"
  } finally {
    loading.value = false
  }
}

async function submit() {
  error.value = ""
  if (!(await invoiceFormRef.value?.validate())) {
    error.value = "Merci de corriger les champs du formulaire"
    return
  }
  saving.value = true
  try {
    const invoice = await invoiceService.update(route.params.id, { title: form.value.title.trim(), total_amount: Number(form.value.totalAmount) })
    await router.push({ name: "InvoiceView", params: { id: invoice.id } })
  } catch (err) {
    error.value = err.response?.data?.detail ?? "Impossible de modifier la facture"
  } finally {
    saving.value = false
  }
}

function goBack() { router.push({ name: "InvoiceView", params: { id: route.params.id } }) }
onMounted(loadInvoice)
</script>

<style scoped>
.loading-container { display: flex; min-height: 400px; align-items: center; justify-content: center; flex-direction: column; gap: 16px; }
</style>
