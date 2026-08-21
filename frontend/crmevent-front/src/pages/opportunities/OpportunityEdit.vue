<template>
  <DashboardLayout>
    <div v-if="loading" class="loading-container"><v-progress-circular indeterminate color="primary" size="48" /><p>Chargement de l'opportunité...</p></div>
    <EditPage v-else title="Modifier l'opportunité" breadcrumb="Opportunités / Modification" :saving="saving" :error="error" @submit="submit" @cancel="goBack">
      <OpportunityForm ref="formRef" v-model="form" editing />
    </EditPage>
  </DashboardLayout>
</template>

<script setup>
import { onMounted, ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import DashboardLayout from "@/layouts/DashboardLayout.vue"
import EditPage from "@/components/common/EditPage.vue"
import OpportunityForm from "@/components/opportunity/OpportunityForm.vue"
import opportunityService from "@/services/opportunityService"

const route = useRoute()
const router = useRouter()
const formRef = ref(null)
const loading = ref(false)
const saving = ref(false)
const error = ref("")
const form = ref({ title: "", amount: null, companyId: null, contactId: null, commercialId: null })

async function loadOpportunity() {
  loading.value = true
  try {
    const item = await opportunityService.getById(route.params.id)
    Object.assign(form.value, { title: item.title ?? "", amount: Number(item.amount), companyId: item.company_id, contactId: item.contact_id, commercialId: item.commercial_id })
  } catch (err) { error.value = err.response?.data?.detail ?? "Impossible de charger l'opportunité" }
  finally { loading.value = false }
}

async function submit() {
  error.value = ""
  if (!(await formRef.value?.validate())) { error.value = "Merci de corriger les champs du formulaire"; return }
  saving.value = true
  try {
    const item = await opportunityService.update(route.params.id, { title: form.value.title.trim(), amount: Number(form.value.amount) })
    await router.push({ name: "OpportunityView", params: { id: item.id } })
  } catch (err) { error.value = err.response?.data?.detail ?? "Impossible de modifier l'opportunité" }
  finally { saving.value = false }
}

function goBack() { router.push({ name: "OpportunityView", params: { id: route.params.id } }) }
onMounted(loadOpportunity)
</script>

<style scoped>
.loading-container { display: flex; min-height: 400px; align-items: center; justify-content: center; flex-direction: column; gap: 16px; }
</style>
