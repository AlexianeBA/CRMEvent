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

      <div class="full-width contacts-header">
        <div class="contacts-title">Contacts existants</div>
        <v-btn
          color="primary"
          variant="tonal"
          size="small"
          prepend-icon="mdi-refresh"
          :loading="loadingContacts"
          @click="loadContacts"
        >
          Rafraîchir
        </v-btn>
      </div>

      <v-autocomplete
        v-model="model.contacts"
        :items="contactOptions"
        item-title="label"
        item-value="id"
        return-object
        label="Sélectionner des contacts"
        multiple
        chips
        closable-chips
        clearable
        :loading="loadingContacts"
        :rules="[rules.atLeastOneContact]"
        class="full-width"
      />

      <p
        v-if="contactError"
        class="full-width contact-error"
      >
        {{ contactError }}
      </p>
    </div>
  </v-form>
</template>

<script setup>
import { onMounted, ref, computed } from "vue"
import contactService from "@/services/contactService"

const model = defineModel({
  type: Object,
  required: true,
})

const formRef = ref(null)
const loadingContacts = ref(false)
const contactError = ref("")
const contacts = ref([])

const rules = {
  required: (value) =>
    Boolean(String(value ?? "").trim()) ||
    "Ce champ est obligatoire",
  atLeastOneContact: (value) =>
    Array.isArray(value) && value.length > 0 ||
    "Sélectionne au moins un contact",
}

const contactOptions = computed(() =>
  contacts.value.map((contact) => ({
    id: contact.id,
    label: `${contact.first_name} ${contact.last_name}`,
  })),
)

async function loadContacts() {
  loadingContacts.value = true
  contactError.value = ""

  try {
    contacts.value = await contactService.getContacts()
  } catch (error) {
    console.error("Erreur chargement contacts :", error)
    contactError.value = "Impossible de charger les contacts"
  } finally {
    loadingContacts.value = false
  }
}

function ensureModelDefaults() {
  if (!Array.isArray(model.value.contacts)) {
    model.value.contacts = []
  }
}

async function validate() {
  ensureModelDefaults()

  if (!formRef.value) {
    return false
  }

  const result = await formRef.value.validate()
  return result.valid
}

function resetValidation() {
  formRef.value?.resetValidation()
}

onMounted(() => {
  ensureModelDefaults()
  loadContacts()
})

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

.contacts-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 8px;
}

.contacts-title {
  font-weight: 600;
  font-size: 1rem;
}

.contact-error {
  color: rgb(var(--v-theme-error));
  margin-top: -8px;
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