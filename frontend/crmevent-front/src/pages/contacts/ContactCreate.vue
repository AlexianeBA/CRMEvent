<template>
  <DashboardLayout>
    <EditPage
      title="Nouveau contact"
      breadcrumb="Contacts / Création"
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
import { ref } from "vue"
import { useRouter } from "vue-router"

import DashboardLayout from "@/layouts/DashboardLayout.vue"
import EditPage from "@/components/common/EditPage.vue"
import ContactForm from "@/components/contact/ContactForm.vue"
import { contactService } from "@/services/contactService"

const router = useRouter()

const contactFormRef = ref(null)

const saving = ref(false)
const error = ref("")

const form = ref({
  firstName: "",
  lastName: "",
  email: "",
  phoneNumber: "",
  companyId: null,
})

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
    const createdContact =
      await contactService.create(buildPayload())

    await router.push({
      name: "ContactView",
      params: { id: createdContact.id },
    })
  } catch (err) {
    console.error(
      "Erreur pendant la création du contact :",
      err,
    )

    error.value =
      err.response?.data?.detail ??
      "Impossible de créer le contact"
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

function normalizeCompanyId(value) {
  if (
    value === null ||
    value === undefined ||
    value === ""
  ) {
    return null
  }

  return Number(value)
}

function normalizeOptionalValue(value) {
  const normalizedValue = String(value ?? "").trim()

  return normalizedValue || null
}

function goBack() {
  router.push({
    name: "Contacts",
  })
}
</script>
