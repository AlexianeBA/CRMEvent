<template>
  <DashboardLayout>
    <EditPage
      title="Nouvelle entreprise"
      breadcrumb="Entreprises / Création"
      :saving="saving"
      :error="error"
      @submit="submit"
      @cancel="goBack"
    >
      <CompanyForm
        ref="companyFormRef"
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
import CompanyForm from "@/components/company/CompanyForm.vue"
import { companyService } from "@/services/companyService"

const router = useRouter()

const companyFormRef = ref(null)

const saving = ref(false)
const error = ref("")

const form = ref({
  name: "",
  address: "",
  city: "",
})

async function submit() {
  error.value = ""

  const isValid =
    await companyFormRef.value?.validate()

  if (!isValid) {
    error.value =
      "Merci de corriger les champs du formulaire"
    return
  }

  saving.value = true

  try {
    const createdCompany =
      await companyService.create(buildPayload())

    if (createdCompany?.id) {
      router.push({
        name: "CompanyView",
        params: {
          id: createdCompany.id,
        },
      })

      return
    }

    router.push({
      name: "Companies",
    })
  } catch (err) {
    console.error(
      "Erreur pendant la création de l'entreprise :",
      err,
    )

    error.value =
      err.response?.data?.detail ??
      "Impossible de créer l'entreprise"
  } finally {
    saving.value = false
  }
}

function buildPayload() {
  return {
    name: form.value.name.trim(),
    address: normalizeOptionalValue(form.value.address),
    city: normalizeOptionalValue(form.value.city),
  }
}

function normalizeOptionalValue(value) {
  const normalizedValue = String(value ?? "").trim()

  return normalizedValue || null
}

function goBack() {
  router.push({
    name: "Companies",
  })
}
</script>
