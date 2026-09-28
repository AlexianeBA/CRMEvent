<template>
  <v-card rounded="xl" elevation="0" border class="mt-6">
    <v-card-title class="d-flex align-center">
      <v-icon icon="mdi-cash-multiple" class="mr-2" /> Paiements
      <v-spacer />
      <v-btn v-if="canAdd" color="primary" prepend-icon="mdi-plus" @click="openDialog">Enregistrer un paiement</v-btn>
    </v-card-title>
    <v-card-text>
      <v-alert v-if="error" type="error" variant="tonal" class="mb-4">{{ error }}</v-alert>
      <v-table v-if="payments.length" density="comfortable">
        <thead><tr><th>Date</th><th>Montant</th><th>Moyen</th><th>Référence</th><th v-if="canDelete" /></tr></thead>
        <tbody>
          <tr v-for="payment in payments" :key="payment.id">
            <td>{{ formatDate(payment.paid_at) }}</td>
            <td>{{ formatCurrency(payment.amount) }}</td>
            <td>{{ methodLabels[payment.payment_method] ?? payment.payment_method }}</td>
            <td>{{ payment.reference || "—" }}</td>
            <td v-if="canDelete" class="text-right"><v-btn icon="mdi-delete-outline" size="small" variant="text" color="error" @click="remove(payment)" /></td>
          </tr>
        </tbody>
      </v-table>
      <div v-else class="text-medium-emphasis py-6 text-center">Aucun paiement enregistré</div>
    </v-card-text>
  </v-card>

  <v-dialog v-model="dialog" max-width="560">
    <v-card title="Enregistrer un paiement">
      <v-card-text>
        <v-form ref="formRef">
          <v-text-field v-model.number="form.amount" label="Montant" type="number" min="0.01" :max="invoice.balance_remaining" step="0.01" suffix="€" :rules="amountRules" />
          <v-text-field v-model="form.paidAt" label="Date du paiement" type="date" :rules="[required]" />
          <v-select v-model="form.paymentMethod" :items="methods" item-title="label" item-value="value" label="Moyen de paiement" :rules="[required]" />
          <v-text-field v-model="form.reference" label="Référence (optionnelle)" />
          <v-textarea v-model="form.notes" label="Notes (optionnelles)" rows="2" />
        </v-form>
      </v-card-text>
      <v-card-actions><v-spacer /><v-btn @click="dialog = false">Annuler</v-btn><v-btn color="primary" :loading="saving" @click="save">Enregistrer</v-btn></v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { computed, ref } from "vue"
import invoiceService from "@/services/invoiceService"

const props = defineProps({ invoice: { type: Object, required: true }, payments: { type: Array, default: () => [] }, canManage: Boolean })
const emit = defineEmits(["updated"])
const dialog = ref(false)
const saving = ref(false)
const error = ref("")
const formRef = ref(null)
const today = () => new Date().toISOString().slice(0, 10)
const form = ref({ amount: null, paidAt: today(), paymentMethod: "bank_transfer", reference: "", notes: "" })
const methods = [{ label: "Virement", value: "bank_transfer" }, { label: "Carte bancaire", value: "card" }, { label: "Chèque", value: "check" }, { label: "Espèces", value: "cash" }, { label: "Autre", value: "other" }]
const methodLabels = Object.fromEntries(methods.map((item) => [item.value, item.label]))
const required = (value) => Boolean(String(value ?? "").trim()) || "Ce champ est obligatoire"
const amountRules = [required, (value) => Number(value) > 0 || "Le montant doit être positif", (value) => Number(value) <= Number(props.invoice.balance_remaining) || "Le montant dépasse le solde"]
const canAdd = computed(() => props.canManage && ["sent", "overdue"].includes(props.invoice.status) && Number(props.invoice.balance_remaining) > 0)
const canDelete = computed(() => props.canManage && props.invoice.status !== "locked")

function openDialog() { form.value = { amount: Number(props.invoice.balance_remaining), paidAt: today(), paymentMethod: "bank_transfer", reference: "", notes: "" }; dialog.value = true }
async function save() {
  if (!(await formRef.value?.validate()).valid) return
  saving.value = true; error.value = ""
  try {
    await invoiceService.addPayment(props.invoice.id, { amount: Number(form.value.amount), paid_at: new Date(`${form.value.paidAt}T12:00:00`).toISOString(), payment_method: form.value.paymentMethod, reference: form.value.reference.trim() || null, notes: form.value.notes.trim() || null })
    dialog.value = false; emit("updated")
  } catch (err) { error.value = err.response?.data?.detail ?? "Impossible d’enregistrer le paiement" }
  finally { saving.value = false }
}
async function remove(payment) {
  if (!window.confirm(`Supprimer le paiement de ${formatCurrency(payment.amount)} ?`)) return
  try { await invoiceService.deletePayment(props.invoice.id, payment.id); emit("updated") }
  catch (err) { error.value = err.response?.data?.detail ?? "Impossible de supprimer le paiement" }
}
const formatCurrency = (value) => new Intl.NumberFormat("fr-FR", { style: "currency", currency: "EUR" }).format(Number(value ?? 0))
const formatDate = (value) => new Intl.DateTimeFormat("fr-FR", { dateStyle: "medium" }).format(new Date(value))
</script>
