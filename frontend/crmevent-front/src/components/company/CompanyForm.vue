<template>
  <v-form
    ref="formRef"
    @submit.prevent
  >
    <div class="form-grid">
      <v-text-field
        v-model="model.name"
        label="Nom de l'entreprise"
        variant="outlined"
        prepend-inner-icon="mdi-domain"
        :rules="[rules.required]"
        class="full-width"
      />

      <v-text-field
        v-model="model.address"
        label="Adresse"
        variant="outlined"
        prepend-inner-icon="mdi-map-marker-outline"
        class="full-width"
      />

      <v-text-field
        v-model="model.city"
        label="Ville"
        variant="outlined"
        prepend-inner-icon="mdi-city"
      />

      <v-text-field
        v-model="model.contact_id"
        label="ID du contact"
        variant="outlined"
        prepend-inner-icon="mdi-account"
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