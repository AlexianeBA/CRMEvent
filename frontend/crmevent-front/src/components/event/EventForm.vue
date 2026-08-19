<template>
  <v-form
    ref="formRef"
    @submit.prevent
  >
    <div class="form-grid">
      <v-text-field
        v-model="model.title"
        label="Titre"
        variant="outlined"
        prepend-inner-icon="mdi-calendar-text"
        :rules="[rules.required]"
        class="full-width"
        />

      <v-text-field
        v-model="model.date"
        label="Date"
        type="date"
        variant="outlined"
        prepend-inner-icon="mdi-calendar"
        :rules="[rules.required]"
        />

      <v-autocomplete
        v-model="model.companyId"
        :items="companies"
        item-title="name"
        item-value="id"
        label="Entreprise"
        variant="outlined"
        prepend-inner-icon="mdi-domain"
        :loading="loadingOptions"
        :rules="[rules.required]"
        clearable
      />

      <v-autocomplete
        v-model="model.opportunityId"
        :items="opportunities"
        item-title="title"
        item-value="id"
        label="Opportunité"
        variant="outlined"
        prepend-inner-icon="mdi-briefcase-outline"
        :loading="loadingOptions"
        :rules="[rules.required]"
        clearable
      />
      <v-autocomplete
        v-model="model.assignedUserId"
        :items="users"
        item-title="email"
        item-value="id"
        label="Utilisateur assigné"
        variant="outlined"
        prepend-inner-icon="mdi-account-tie-outline"
        :loading="loadingOptions"
        :rules="[rules.required]"
        clearable
      />
    <v-select
        v-model="model.type"
        :items="eventTypes"
        item-title="label"
        item-value="value"
        label="Type d'événement"
        variant="outlined"
        prepend-inner-icon="mdi-shape-outline"
        :rules="[rules.required]"
    />
    <v-text-field
        v-model.number="model.duration"
        label="Durée en heures"
        type="number"
        min="1"
        variant="outlined"
        prepend-inner-icon="mdi-clock-outline"
        :rules="[rules.required, rules.positiveNumber]"
    />
    <v-select
        v-model="model.status"
        :items="['draft', 'scheduled', 'held', 'canceled', 'locked']"
        label="Statut"
        variant="outlined"
        prepend-inner-icon="mdi-flag-outline"
        :rules="[rules.required]"
    />
    <v-text-field
        v-model="model.location"
        label="Localisation"
        variant="outlined"
        prepend-inner-icon="mdi-map-marker-outline"
        :rules="[rules.required]"
    />

    <v-textarea
            v-model="model.description"
            label="Description"
            variant="outlined"
            prepend-inner-icon="mdi-text"
            rows="4"
            counter="255"
            class="full-width"
        />
      <v-autocomplete
        v-model="model.contactId"
        :items="contactOptions"
        item-title="label"
        item-value="id"
        label="Contact (optionnel)"
        variant="outlined"
        prepend-inner-icon="mdi-account-outline"
        :loading="loadingOptions"
        clearable
      />
        
    </div>
  </v-form>
</template>

<script setup>
import { computed, onMounted, ref, } from "vue"
import companyService from "@/services/companyService"
import contactService from "@/services/contactService"
import opportunityService from "@/services/opportunityService"
import userService from "@/services/userService"


const model = defineModel({
  type: Object,
  required: true,
})

const formRef = ref(null)

const companies = ref([])
const opportunities = ref([])
const users = ref([])
const contacts = ref([])
const loadingOptions = ref(false)
const optionsError = ref("")

const rules = {
  required: (value) =>
    Boolean(String(value ?? "").trim()) ||
    "Ce champ est obligatoire",
    positiveNumber: (value) =>
        Number(value) > 0 ||
        "La valeur doit être supérieure à 0",
}
const eventTypes = [
  { label: "Webinaire", value: "webinar" },
  { label: "Atelier", value: "workshop" },
  { label: "Conférence", value: "conference" },
]

const contactOptions = computed(() =>
  contacts.value.map((contact) => ({
    id: contact.id,
    label: [contact.first_name, contact.last_name]
      .filter(Boolean)
      .join(" "),
  })),
)

async function loadOptions() {
  loadingOptions.value = true
  optionsError.value = ""

  try {
    const [
      companyList,
      opportunityList,
      userList,
      contactList,
    ] = await Promise.all([
      companyService.getCompanies(),
      opportunityService.getOpportunities(),
      userService.getUsers(),
      contactService.getContacts(),
    ])

    companies.value = companyList
    opportunities.value = opportunityList
    users.value = userList
    contacts.value = contactList
  } catch (error) {
    console.error(
      "Erreur de chargement des listes :",
      error,
    )

    optionsError.value =
      error.response?.data?.detail ??
      "Impossible de charger les listes"
  } finally {
    loadingOptions.value = false
  }
}



async function validate() {
  if (!formRef.value) {
    return false
  }

  const result = await formRef.value.validate()

  return result.valid
}

function resetValidation() {
  formRef.value?.resetValidation()
}

onMounted(loadOptions)

defineExpose({
  validate,
  resetValidation,
})
</script>

<style scoped>
.form-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 4px 20px;
}

.full-width {
  grid-column: 1 / -1;
}

@media (max-width: 750px) {
  .form-grid {
    grid-template-columns: 1fr;
  }

  .full-width {
    grid-column: auto;
  }
}
</style>