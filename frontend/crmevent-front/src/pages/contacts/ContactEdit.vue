<template>
  <DashboardLayout>
    <div
      v-if="loading"
      class="loading-container"
    >
      <v-progress-circular
        indeterminate
        color="primary"
        size="48"
      />

      <p>Chargement du contact...</p>
    </div>

    <EditPage
      v-else
      title="Modifier le contact"
      breadcrumb="Contacts / Modification"
      :saving="saving"
      :error="error"
      @submit="submit"
      @cancel="goBack"
    >
      <ContactForm
        ref="contactFormRef"
        v-model="form"
      />
    </EditPage>
  </DashboardLayout>
</template>

<script setup>
import { onMounted, ref } from "vue"
import { useRoute, useRouter } from "vue-router"

import DashboardLayout from "@/layouts/DashboardLayout.vue"
import EditPage from "@/components/common/EditPage.vue"
import ContactForm from "@/components/contact/ContactForm.vue"
import { contactService } from "@/services/contactService"

const route = useRoute()
const router = useRouter()

const contactFormRef = ref(null)

const loading = ref(false)
const saving = ref(false)
const error = ref("")

const form = ref({
  firstName: "",
  lastName: "",
  email: "",
  phoneNumber: "",
  companyId: null,
})

async function loadContact() {
  const contactId = route.params.id

  if (!contactId) {
    error.value = "L'identifiant du contact est manquant"
    return
  }

  loading.value = true
  error.value = ""

  try {
    const contact = await contactService.getById(contactId)

    Object.assign(form.value, {
    firstName: contact.first_name ?? "",
    lastName: contact.last_name ?? "",
    email: contact.email ?? "",
    phoneNumber: contact.phone_number ?? "",
    companyId: contact.company_id ?? null,
    })
    } catch (err) {
    console.error(
      "Erreur pendant le chargement du contact :",
      err,
    )

    error.value =
      err.response?.data?.detail ??
      "Impossible de charger le contact"
  } finally {
    loading.value = false
  }
}

async function submit() {
  error.value = ""

  const isValid =
    await contactFormRef.value?.validate()

  if (!isValid) {
    error.value =
      "Merci de corriger les champs du formulaire"
    return
  }

  saving.value = true

  try {
    const updatedContact =
      await contactService.update(
        route.params.id,
        buildPayload(),
      )

    router.push({
      name: "ContactView",
      params: {
        id: updatedContact?.id ?? route.params.id,
      },
    })
  } catch (err) {
    console.error(
      "Erreur pendant la modification du contact :",
      err,
    )

    error.value =
      err.response?.data?.detail ??
      "Impossible de modifier le contact"
  } finally {
    saving.value = false
  }
}

function buildPayload() {
  return {
    first_name: form.value.firstName.trim(),
    last_name: form.value.lastName.trim(),
    email: normalizeOptionalValue(
      form.value.email,
    ),
    phone_number: normalizeOptionalValue(
      form.value.phoneNumber,
    ),
    company_id: normalizeCompanyId(
      form.value.companyId,
    ),
  }
}

function normalizeOptionalValue(value) {
  const normalizedValue = String(value ?? "").trim()

  return normalizedValue || null
}

function normalizeCompanyId(value) {
  if (value === null || value === undefined || value === "") {
    return null
  }

  return Number(value)
}

function goBack() {
  router.push({
    name: "ContactView",
    params: {
      id: route.params.id,
    },
  })
}

onMounted(loadContact)
</script>

<style scoped>
.loading-container {
  display: flex;
  min-height: 400px;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  gap: 16px;
}

.loading-container p {
  margin: 0;
  color: #6b7280;
}
</style>
