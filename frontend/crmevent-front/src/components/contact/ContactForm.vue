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
        :rules="[rules.required]"
        class="full-width"
      />
        <v-text-field
          v-model="model.companyId"
          label="ID de l'entreprise (optionnel)"
          type="number"
          variant="outlined"
          prepend-inner-icon="mdi-domain"
          class="full-width"
        />
        
    </div>
  </v-form>
</template>

<script setup>
import { ref } from "vue"

const model = defineModel({
  type: Object,
  required: true,
})

const formRef = ref(null)

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