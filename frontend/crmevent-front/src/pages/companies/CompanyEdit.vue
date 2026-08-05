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

      <p>Chargement de l'entreprise...</p>
    </div>

    <EditPage
      v-else
      title="Modifier l'entreprise"
      breadcrumb="Entreprises / Modification"
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
import { onMounted, ref } from "vue"
import { useRoute, useRouter } from "vue-router"

import DashboardLayout from "@/layouts/DashboardLayout.vue"
import EditPage from "@/components/common/EditPage.vue"
import CompanyForm from "@/components/company/CompanyForm.vue"
import { companyService } from "@/services/companyService"

const route = useRoute()
const router = useRouter()

const companyFormRef = ref(null)

const loading = ref(false)
const saving = ref(false)
const error = ref("")

const form = ref({
  name: "",
  address: "",
  city: "",
})

async function loadCompany() {
  const companyId = route.params.id

  if (!companyId) {
    error.value = "L'identifiant de l'entreprise est manquant"
    return
  }

  loading.value = true
  error.value = ""

  try {
    const company = await companyService.getById(companyId)

    Object.assign(form.value, {
      name: company.name ?? "",
      address: company.address ?? "",
      city: company.city ?? "",
    })
  } catch (err) {
    console.error(
      "Erreur pendant le chargement de l'entreprise :",
      err,
    )

    error.value =
      err.response?.data?.detail ??
      "Impossible de charger l'entreprise"
  } finally {
    loading.value = false
  }
}

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
    const updatedCompany =
      await companyService.update(
        route.params.id,
        buildPayload(),
      )

    router.push({
      name: "CompanyView",
      params: {
        id: updatedCompany?.id ?? route.params.id,
      },
    })
  } catch (err) {
    console.error(
      "Erreur pendant la modification de l'entreprise :",
      err,
    )

    error.value =
      err.response?.data?.detail ??
      "Impossible de modifier l'entreprise"
  } finally {
    saving.value = false
  }
}

function buildPayload() {
  return {
    name: form.value.name.trim(),
    email: normalizeOptionalValue(form.value.email),
    phone: normalizeOptionalValue(form.value.phone),
    website: normalizeOptionalValue(form.value.website),
    address: normalizeOptionalValue(form.value.address),
    postal_code: normalizeOptionalValue(
      form.value.postal_code,
    ),
    city: normalizeOptionalValue(form.value.city),
    country: normalizeOptionalValue(form.value.country),
  }
}

function normalizeOptionalValue(value) {
  const normalizedValue = String(value ?? "").trim()

  return normalizedValue || null
}

function goBack() {
  router.push({
    name: "CompanyView",
    params: {
      id: route.params.id,
    },
  })
}

onMounted(loadCompany)
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
