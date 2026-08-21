<template>
  <v-form ref="formRef" @submit.prevent>
    <div class="form-grid">
      <v-text-field v-model="model.title" label="Titre de l'opportunité" variant="outlined" prepend-inner-icon="mdi-briefcase-outline" :rules="[rules.required]" class="full-width" />
      <v-text-field v-model.number="model.amount" label="Montant estimé" type="number" min="0.01" step="0.01" suffix="€" variant="outlined" prepend-inner-icon="mdi-currency-eur" :rules="[rules.required, rules.positiveAmount]" />
      <v-autocomplete v-model="model.companyId" :items="companies" item-title="name" item-value="id" label="Entreprise" variant="outlined" prepend-inner-icon="mdi-domain" :loading="loadingOptions" :disabled="editing" :rules="[rules.required]" clearable @update:model-value="onCompanyChange" />
      <v-autocomplete v-model="model.contactId" :items="contactOptions" item-title="label" item-value="id" label="Contact" variant="outlined" prepend-inner-icon="mdi-account-outline" :loading="loadingOptions" :disabled="editing || !model.companyId" :rules="[rules.required]" clearable />
      <v-autocomplete v-model="model.commercialId" :items="users" item-title="email" item-value="id" label="Commercial" variant="outlined" prepend-inner-icon="mdi-account-tie-outline" :loading="loadingOptions" :disabled="editing" :rules="[rules.required]" clearable />
      <v-alert v-if="optionsError" type="error" variant="tonal" class="full-width">{{ optionsError }}</v-alert>
    </div>
  </v-form>
</template>

<script setup>
import { computed, onMounted, ref } from "vue"
import companyService from "@/services/companyService"
import contactService from "@/services/contactService"
import userService from "@/services/userService"

const model = defineModel({ type: Object, required: true })
const props = defineProps({ editing: { type: Boolean, default: false } })
const formRef = ref(null)
const companies = ref([])
const contacts = ref([])
const users = ref([])
const loadingOptions = ref(false)
const optionsError = ref("")
const rules = {
  required: (value) => Boolean(String(value ?? "").trim()) || "Ce champ est obligatoire",
  positiveAmount: (value) => Number(value) > 0 || "Le montant doit être supérieur à 0",
}

const contactOptions = computed(() => contacts.value
  .filter((contact) => !model.value.companyId || contact.company_id === model.value.companyId)
  .map((contact) => ({ id: contact.id, label: `${contact.first_name} ${contact.last_name}` })))

function onCompanyChange() {
  if (!props.editing) model.value.contactId = null
}

async function loadOptions() {
  loadingOptions.value = true
  try {
    const [companyList, contactList, userList] = await Promise.all([companyService.getCompanies(), contactService.getContacts(), userService.getUsers()])
    companies.value = companyList
    contacts.value = contactList
    users.value = userList
  } catch (error) {
    optionsError.value = error.response?.data?.detail ?? "Impossible de charger les listes"
  } finally { loadingOptions.value = false }
}

async function validate() {
  if (!formRef.value) return false
  return (await formRef.value.validate()).valid
}

onMounted(loadOptions)
defineExpose({ validate })
</script>

<style scoped>
.form-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 4px 20px; }
.full-width { grid-column: 1 / -1; }
@media (max-width: 750px) { .form-grid { grid-template-columns: 1fr; } .full-width { grid-column: auto; } }
</style>
