<template>
  <v-form
    ref="formRef"
    @submit.prevent
  >
    <div class="form-grid">
      <v-text-field
        v-model="model.firstName"
        label="Prénom"
        variant="outlined"
        prepend-inner-icon="mdi-account"
        :rules="[rules.required]"
        class="full-width"
      />

      <v-text-field
        v-model="model.lastName"
        label="Nom"
        variant="outlined"
        prepend-inner-icon="mdi-account"
        :rules="[rules.required]"
        class="full-width"
      />

      <v-text-field
        v-model="model.email"
        label="Email"
        variant="outlined"
        prepend-inner-icon="mdi-email-outline"
        :rules="[rules.required, rules.email]"
        class="full-width"
      />

      <v-text-field
        v-model="model.phoneNumber"
        label="Numéro de téléphone"
        variant="outlined"
        prepend-inner-icon="mdi-phone-outline"
        class="full-width"
      />
        <v-autocomplete
          v-model="model.companyId"
          :items="companies"
          item-title="name"
          item-value="id"
          label="Entreprise (optionnelle)"
          variant="outlined"
          prepend-inner-icon="mdi-domain"
          :loading="loadingCompanies"
          clearable
          class="full-width"
        />

      <p v-if="companiesError" class="full-width form-error">
        {{ companiesError }}
      </p>
        
    </div>
  </v-form>
</template>

<script setup>
import { onMounted, ref } from "vue"
import companyService from "@/services/companyService"

const model = defineModel({
  type: Object,
  required: true,
})

const formRef = ref(null)
const companies = ref([])
const loadingCompanies = ref(false)
const companiesError = ref("")

const rules = {
  required: (value) =>
    Boolean(String(value ?? "").trim()) ||
    "Ce champ est obligatoire",

  email: (value) => {
    if (!value) {
      return true
    }

    const emailPattern =
      /^[^\s@]+@[^\s@]+\.[^\s@]+$/

    return (
      emailPattern.test(value) ||
      "L'adresse email n'est pas valide"
    )
  },
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

async function loadCompanies() {
  loadingCompanies.value = true
  companiesError.value = ""

  try {
    companies.value = await companyService.getCompanies()
  } catch (error) {
    console.error("Erreur de chargement des entreprises :", error)
    companiesError.value = "Impossible de charger les entreprises"
  } finally {
    loadingCompanies.value = false
  }
}

onMounted(loadCompanies)

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

.form-error {
  color: rgb(var(--v-theme-error));
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
