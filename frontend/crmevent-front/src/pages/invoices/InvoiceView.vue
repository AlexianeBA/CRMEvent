<template>
  <DashboardLayout>
    <DetailPage :title="invoice?.number || 'Facture'" :subtitle="invoice?.title" breadcrumb="Factures / Détail" :loading="loading" :error="error" :show-edit="canEdit" @back="goToList" @edit="goToEdit">
      <template #actions>
        <v-btn v-if="invoice" variant="tonal" prepend-icon="mdi-file-pdf-box" :loading="downloading" @click="downloadPdf">Télécharger PDF</v-btn>
        <v-btn v-if="auth.canManageInvoices && invoice?.status === 'draft'" color="primary" prepend-icon="mdi-send-outline" :loading="actionLoading" @click="changeStatus('sent')">Envoyer</v-btn>
        <v-btn v-if="auth.canManageInvoices && ['draft', 'sent', 'overdue'].includes(invoice?.status)" color="error" variant="tonal" prepend-icon="mdi-cancel" :loading="actionLoading" @click="changeStatus('canceled')">Annuler</v-btn>
        <v-btn v-if="auth.canManageInvoices && ['paid', 'canceled'].includes(invoice?.status)" variant="tonal" prepend-icon="mdi-lock-outline" :loading="actionLoading" @click="changeStatus('locked')">Verrouiller</v-btn>
        <v-btn v-if="auth.canManageInvoices && ['draft', 'canceled'].includes(invoice?.status)" color="error" variant="tonal" prepend-icon="mdi-delete-outline" :loading="actionLoading" @click="deleteInvoice">Supprimer</v-btn>
      </template>
      <InvoiceDetails v-if="invoice" :invoice="invoice" />
      <InvoicePayments v-if="invoice" :invoice="invoice" :payments="payments" :can-manage="auth.canManageInvoices" @updated="reloadBilling" />
      <HistoryTimeline v-if="invoice" entity-type="invoice" :entity-id="invoice.id" />
    </DetailPage>
  </DashboardLayout>
</template>

<script setup>
import { computed, onMounted, ref, watch } from "vue"
import { useRoute, useRouter } from "vue-router"
import DashboardLayout from "@/layouts/DashboardLayout.vue"
import DetailPage from "@/components/common/DetailPage.vue"
import InvoiceDetails from "@/components/invoice/InvoiceDetails.vue"
import InvoicePayments from "@/components/invoice/InvoicePayments.vue"
import invoiceService from "@/services/invoiceService"
import { useAuthStore } from "@/stores/auth"
import HistoryTimeline from "@/components/history/HistoryTimeline.vue"
import { downloadResponse } from "@/utils/download"

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const invoice = ref(null)
const payments = ref([])
const loading = ref(false)
const actionLoading = ref(false)
const downloading = ref(false)
const error = ref("")
const canEdit = computed(() => auth.canManageInvoices && invoice.value?.status === "draft")

async function loadInvoice() {
  loading.value = true
  error.value = ""
  try {
    const [invoiceResult, paymentResult] = await Promise.all([invoiceService.getById(route.params.id), invoiceService.getPayments(route.params.id)])
    invoice.value = invoiceResult
    payments.value = paymentResult
  }
  catch (err) { error.value = err.response?.data?.detail ?? "Impossible de charger la facture" }
  finally { loading.value = false }
}

async function runAction(action) {
  actionLoading.value = true
  error.value = ""
  try { await action() }
  catch (err) { error.value = err.response?.data?.detail ?? "Impossible d'effectuer cette action" }
  finally { actionLoading.value = false }
}

function changeStatus(status) {
  return runAction(async () => { invoice.value = await invoiceService.updateStatus(route.params.id, status) })
}

async function reloadBilling() { await loadInvoice() }

async function downloadPdf() {
  downloading.value = true
  error.value = ""
  try { downloadResponse(await invoiceService.downloadPdf(invoice.value.id), `${invoice.value.number}.pdf`) }
  catch (err) { error.value = err.response?.data?.detail ?? "Impossible de télécharger la facture" }
  finally { downloading.value = false }
}

async function deleteInvoice() {
  if (!window.confirm(`Supprimer la facture ${invoice.value.number} ?`)) return
  await runAction(async () => { await invoiceService.delete(route.params.id); await router.push({ name: "Invoices" }) })
}

function goToList() { router.push({ name: "Invoices" }) }
function goToEdit() { router.push({ name: "InvoiceEdit", params: { id: route.params.id } }) }
watch(() => route.params.id, (newId, oldId) => { if (newId && newId !== oldId) loadInvoice() })
onMounted(loadInvoice)
</script>
