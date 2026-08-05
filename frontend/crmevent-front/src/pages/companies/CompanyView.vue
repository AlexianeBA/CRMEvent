<template>
  <DashboardLayout>
    <DetailPage
      :title="company?.name || 'Détail de l’entreprise'"
      breadcrumb="Entreprises / Détail"
      :loading="loading"
      :error="error"
      @back="goToList"
      @edit="goToEdit"
    >
      <CompanyDetails
        v-if="company"
        :company="company"
      />
    </DetailPage>
  </DashboardLayout>
</template>

<script setup>
import { onMounted, ref, watch } from "vue"
import { useRoute, useRouter } from "vue-router"

import DashboardLayout from "@/layouts/DashboardLayout.vue"
import DetailPage from "@/components/common/DetailPage.vue"
import CompanyDetails from "@/components/company/CompanyDetails.vue"
import { companyService } from "@/services/companyService"

const route = useRoute()
const router = useRouter()

const company = ref(null)
const loading = ref(false)
const error = ref("")

async function loadCompany() {
  const companyId = route.params.id

  if (!companyId) {
    error.value = "L'identifiant de l'entreprise est manquant"
    return
  }

  loading.value = true
  error.value = ""
  company.value = null

  try {
    company.value = await companyService.getById(companyId)
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

function goToList() {
  router.push({
    name: "Companies",
  })
}

function goToEdit() {
  router.push({
    name: "CompanyEdit",
    params: {
      id: route.params.id,
    },
  })
}

watch(
  () => route.params.id,
  (newId, oldId) => {
    if (newId && newId !== oldId) {
      loadCompany()
    }
  },
)

onMounted(loadCompany)
</script>