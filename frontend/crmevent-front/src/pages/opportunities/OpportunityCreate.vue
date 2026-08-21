<template>
  <DashboardLayout>
    <EditPage title="Nouvelle opportunité" breadcrumb="Opportunités / Création" :saving="saving" :error="error" @submit="submit" @cancel="goBack">
      <OpportunityForm ref="formRef" v-model="form" />
    </EditPage>
  </DashboardLayout>
</template>

<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import DashboardLayout from "@/layouts/DashboardLayout.vue"
import EditPage from "@/components/common/EditPage.vue"
import OpportunityForm from "@/components/opportunity/OpportunityForm.vue"
import opportunityService from "@/services/opportunityService"

const router = useRouter()
const formRef = ref(null)
const saving = ref(false)
const error = ref("")
const form = ref({ title: "", amount: null, companyId: null, contactId: null, commercialId: null })

async function submit() {
  error.value = ""
  if (!(await formRef.value?.validate())) { error.value = "Merci de corriger les champs du formulaire"; return }
  saving.value = true
  try {
    const opportunity = await opportunityService.create({ title: form.value.title.trim(), amount: Number(form.value.amount), company_id: Number(form.value.companyId), contact_id: Number(form.value.contactId), commercial_id: Number(form.value.commercialId) })
    await router.push({ name: "OpportunityView", params: { id: opportunity.id } })
  } catch (err) { error.value = err.response?.data?.detail ?? "Impossible de créer l'opportunité" }
  finally { saving.value = false }
}

function goBack() { router.push({ name: "Opportunities" }) }
</script>
