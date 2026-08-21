<template>
  <v-form ref="formRef" @submit.prevent>
    <div class="form-grid">
      <v-text-field v-model="model.title" label="Titre de la facture" variant="outlined" prepend-inner-icon="mdi-receipt-text-outline" :rules="[rules.required]" class="full-width" />
      <v-text-field v-model.number="model.totalAmount" label="Montant total" type="number" min="0.01" step="0.01" suffix="€" variant="outlined" prepend-inner-icon="mdi-currency-eur" :rules="[rules.required, rules.positiveAmount]" />
    </div>
  </v-form>
</template>

<script setup>
import { ref } from "vue"

const model = defineModel({ type: Object, required: true })
const formRef = ref(null)
const rules = {
  required: (value) => Boolean(String(value ?? "").trim()) || "Ce champ est obligatoire",
  positiveAmount: (value) => Number(value) > 0 || "Le montant doit être supérieur à 0",
}

async function validate() {
  if (!formRef.value) return false
  return (await formRef.value.validate()).valid
}

defineExpose({ validate })
</script>

<style scoped>
.form-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 4px 20px; }
.full-width { grid-column: 1 / -1; }
@media (max-width: 750px) { .form-grid { grid-template-columns: 1fr; } .full-width { grid-column: auto; } }
</style>
