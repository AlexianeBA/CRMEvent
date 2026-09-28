<template>
  <v-form ref="formRef" @submit.prevent>
    <div class="form-grid">
      <v-text-field v-model="model.title" label="Titre" variant="outlined" prepend-inner-icon="mdi-clipboard-text-outline" :rules="[rules.required]" class="full-width" />
      <v-select v-model="model.priority" :items="priorities" item-title="label" item-value="value" label="Priorité" variant="outlined" prepend-inner-icon="mdi-flag-outline" />
      <v-text-field v-model="model.dueAt" type="datetime-local" label="Échéance" variant="outlined" prepend-inner-icon="mdi-calendar-clock" :rules="[rules.required, rules.future]" />
      <v-autocomplete v-model="model.assignedUserId" :items="users" item-title="email" item-value="id" label="Utilisateur assigné" variant="outlined" :loading="loading" :rules="[rules.required]" />
      <v-autocomplete v-model="model.opportunityId" :items="opportunities" item-title="title" item-value="id" label="Opportunité" variant="outlined" :loading="loading" clearable />
      <v-autocomplete v-model="model.eventId" :items="filteredEvents" item-title="title" item-value="id" label="Événement" variant="outlined" :loading="loading" clearable />
      <v-textarea v-model="model.description" label="Description" variant="outlined" rows="4" counter="2000" class="full-width" />
      <v-alert v-if="optionsError" type="error" variant="tonal" class="full-width">{{ optionsError }}</v-alert>
    </div>
  </v-form>
</template>

<script setup>
import { computed, onMounted, ref } from "vue"
import eventService from "@/services/eventService"
import opportunityService from "@/services/opportunityService"
import userService from "@/services/userService"

const model = defineModel({ type: Object, required: true })
const formRef = ref(null)
const users = ref([])
const opportunities = ref([])
const events = ref([])
const loading = ref(false)
const optionsError = ref("")
const priorities = [
  { label: "Faible", value: "low" },
  { label: "Normale", value: "medium" },
  { label: "Haute", value: "high" },
]
const filteredEvents = computed(() => model.value.opportunityId
  ? events.value.filter((event) => event.opportunity_id === model.value.opportunityId)
  : events.value)
const rules = {
  required: (value) => Boolean(String(value ?? "").trim()) || "Ce champ est obligatoire",
  future: (value) => !value || new Date(value) > new Date() || "L'échéance doit être dans le futur",
}

async function loadOptions() {
  loading.value = true
  try {
    ;[users.value, opportunities.value, events.value] = await Promise.all([
      userService.getUsers(), opportunityService.getOpportunities(), eventService.getEvents(),
    ])
  } catch (error) {
    optionsError.value = error.response?.data?.detail ?? "Impossible de charger les listes"
  } finally {
    loading.value = false
  }
}

async function validate() {
  const result = await formRef.value?.validate()
  if (!result?.valid) return false
  if (!model.value.opportunityId && !model.value.eventId) {
    optionsError.value = "Sélectionnez une opportunité ou un événement"
    return false
  }
  return true
}

onMounted(loadOptions)
defineExpose({ validate })
</script>

<style scoped>
.form-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 4px 20px; }
.full-width { grid-column: 1 / -1; }
@media (max-width: 750px) { .form-grid { grid-template-columns: 1fr; } .full-width { grid-column: auto; } }
</style>
