<template>
  <v-form ref="formRef" @submit.prevent>
    <div class="form-grid">
      <v-text-field v-model="model.title" label="Titre du devis" variant="outlined" prepend-inner-icon="mdi-file-document-outline" :rules="[rules.required]" class="full-width" />
      <v-text-field v-model.number="model.totalAmount" label="Montant total" type="number" min="0.01" step="0.01" suffix="€" variant="outlined" prepend-inner-icon="mdi-currency-eur" :rules="[rules.required, rules.positiveAmount]" />
      <v-autocomplete v-model="model.companyId" :items="companies" item-title="name" item-value="id" label="Entreprise" variant="outlined" prepend-inner-icon="mdi-domain" :loading="loadingOptions" :disabled="editing" :rules="[rules.required]" clearable />
      <v-autocomplete v-model="model.opportunityId" :items="filteredOpportunities" item-title="title" item-value="id" label="Opportunité" variant="outlined" prepend-inner-icon="mdi-briefcase-outline" :loading="loadingOptions" :disabled="editing" :rules="[rules.required]" clearable />
      <v-autocomplete v-model="model.assignedUserId" :items="users" item-title="email" item-value="id" label="Utilisateur assigné" variant="outlined" prepend-inner-icon="mdi-account-tie-outline" :loading="loadingOptions" :disabled="editing" :rules="[rules.required]" clearable />
      <v-autocomplete v-model="model.eventId" :items="filteredEvents" item-title="title" item-value="id" label="Événement (optionnel)" variant="outlined" prepend-inner-icon="mdi-calendar-outline" :loading="loadingOptions" :disabled="editing" clearable />
      <v-alert v-if="optionsError" type="error" variant="tonal" class="full-width">{{ optionsError }}</v-alert>
    </div>
  </v-form>
</template>

<script setup>
import { computed, onMounted, ref } from "vue"
import companyService from "@/services/companyService"
import eventService from "@/services/eventService"
import opportunityService from "@/services/opportunityService"
import userService from "@/services/userService"

const model = defineModel({ type: Object, required: true })
defineProps({ editing: { type: Boolean, default: false } })

const formRef = ref(null)
const companies = ref([])
const opportunities = ref([])
const users = ref([])
const events = ref([])
const loadingOptions = ref(false)
const optionsError = ref("")

const rules = {
  required: (value) => Boolean(String(value ?? "").trim()) || "Ce champ est obligatoire",
  positiveAmount: (value) => Number(value) > 0 || "Le montant doit être supérieur à 0",
}

const filteredOpportunities = computed(() => {
  if (!model.value.companyId) return []
  return opportunities.value.filter(
    (opportunity) => opportunity.company_id === model.value.companyId,
  )
})

const filteredEvents = computed(() => {
  if (!model.value.companyId || !model.value.opportunityId) return []
  return events.value.filter(
    (event) => event.company_id === model.value.companyId
      && event.opportunity_id === model.value.opportunityId,
  )
})

async function loadOptions() {
  loadingOptions.value = true
  optionsError.value = ""
  try {
    const [companyList, opportunityList, userList, eventList] = await Promise.all([
      companyService.getCompanies(),
      opportunityService.getOpportunities(),
      userService.getUsers(),
      eventService.getEvents(),
    ])
    companies.value = companyList
    opportunities.value = opportunityList
    users.value = userList
    events.value = eventList
  } catch (error) {
    console.error("Erreur de chargement des listes du devis :", error)
    optionsError.value = error.response?.data?.detail ?? "Impossible de charger les listes"
  } finally {
    loadingOptions.value = false
  }
}

async function validate() {
  if (!formRef.value) return false
  return (await formRef.value.validate()).valid
}

function resetValidation() {
  formRef.value?.resetValidation()
}

onMounted(loadOptions)
defineExpose({ validate, resetValidation })
</script>

<style scoped>
.form-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 4px 20px; }
.full-width { grid-column: 1 / -1; }
@media (max-width: 750px) { .form-grid { grid-template-columns: 1fr; } .full-width { grid-column: auto; } }
</style>
