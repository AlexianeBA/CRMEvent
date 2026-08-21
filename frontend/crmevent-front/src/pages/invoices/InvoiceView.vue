<template>
  <DashboardLayout>
    <DetailPage :title="invoice?.number || 'Facture'" :subtitle="invoice?.title" breadcrumb="Factures / Détail" :loading="loading" :error="error" :show-edit="canEdit" @back="goToList" @edit="goToEdit">
      <template #actions>
        <v-btn v-if="invoice?.status === 'draft'" color="primary" prepend-icon="mdi-send-outline" :loading="actionLoading" @click="changeStatus('sent')">Envoyer</v-btn>
        <v-btn v-if="['sent', 'overdue'].includes(invoice?.status)" color="success" prepend-icon="mdi-cash-check" :loading="actionLoading" @click="changeStatus('paid')">Marquer payée</v-btn>
        <v-btn v-if="invoice?.status === 'sent'" color="warning" variant="tonal" prepend-icon="mdi-clock-alert-outline" :loading="actionLoading" @click="changeStatus('overdue')">En retard</v-btn>
        <v-btn v-if="['draft', 'sent', 'overdue'].includes(invoice?.status)" color="error" variant="tonal" prepend-icon="mdi-cancel" :loading="actionLoading" @click="changeStatus('canceled')">Annuler</v-btn>
        <v-btn v-if="['paid', 'canceled'].includes(invoice?.status)" variant="tonal" prepend-icon="mdi-lock-outline" :loading="actionLoading" @click="changeStatus('locked')">Verrouiller</v-btn>
        <v-btn v-if="['draft', 'canceled'].includes(invoice?.status)" color="error" variant="tonal" prepend-icon="mdi-delete-outline" :loading="actionLoading" @click="deleteInvoice">Supprimer</v-btn>
      </template>
      <InvoiceDetails v-if="invoice" :invoice="invoice" />
    </DetailPage>
  </DashboardLayout>
</template>

<script setup>
import { computed, onMounted, ref, watch } from "vue"
import { useRoute, useRouter } from "vue-router"
import DashboardLayout from "@/layouts/DashboardLayout.vue"
import DetailPage from "@/components/common/DetailPage.vue"
import InvoiceDetails from "@/components/invoice/InvoiceDetails.vue"
import invoiceService from "@/services/invoiceService"

const route = useRoute()
const router = useRouter()
const invoice = ref(null)
const loading = ref(false)
const actionLoading = ref(false)
const error = ref("")
const canEdit = computed(() => invoice.value?.status === "draft")

async function loadInvoice() {
  loading.value = true
  error.value = ""
  try { invoice.value = await invoiceService.getById(route.params.id) }
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

async function deleteInvoice() {
  if (!window.confirm(`Supprimer la facture ${invoice.value.number} ?`)) return
  await runAction(async () => { await invoiceService.delete(route.params.id); await router.push({ name: "Invoices" }) })
}

function goToList() { router.push({ name: "Invoices" }) }
function goToEdit() { router.push({ name: "InvoiceEdit", params: { id: route.params.id } }) }
watch(() => route.params.id, (newId, oldId) => { if (newId && newId !== oldId) loadInvoice() })
onMounted(loadInvoice)
</script>
