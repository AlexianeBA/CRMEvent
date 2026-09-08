<template>
  <DashboardLayout>
    <DetailPage :title="opportunity?.title || 'Opportunité'" breadcrumb="Opportunités / Détail" :loading="loading" :error="error" :show-edit="auth.canManageCrm && !isFinal" @back="goToList" @edit="goToEdit">
      <template #actions>
        <v-btn v-for="transition in auth.canManageCrm ? transitions : []" :key="transition.status" :color="transition.color" :variant="transition.variant" :prepend-icon="transition.icon" :loading="actionLoading" @click="runTransition(transition)">{{ transition.label }}</v-btn>
        <v-btn v-if="auth.canManageCrm && opportunity?.status === 'closed_won'" color="primary" prepend-icon="mdi-calendar-plus" @click="createEvent">Créer l'événement</v-btn>
        <v-btn v-if="auth.canDeleteCrm && !isFinal" color="error" variant="tonal" prepend-icon="mdi-delete-outline" :loading="actionLoading" @click="deleteOpportunity">Supprimer</v-btn>
      </template>
      <OpportunityDetails v-if="opportunity" :opportunity="opportunity" />
      <OpportunityActivities
        v-if="opportunity"
        :opportunity-id="opportunity.id"
        @changed="historyVersion += 1"
      />
      <HistoryTimeline
        v-if="opportunity"
        :key="historyVersion"
        entity-type="opportunity"
        :entity-id="opportunity.id"
      />
    </DetailPage>
  </DashboardLayout>
</template>

<script setup>
import { computed, onMounted, ref, watch } from "vue"
import { useRoute, useRouter } from "vue-router"
import DashboardLayout from "@/layouts/DashboardLayout.vue"
import DetailPage from "@/components/common/DetailPage.vue"
import OpportunityDetails from "@/components/opportunity/OpportunityDetails.vue"
import opportunityService from "@/services/opportunityService"
import { useAuthStore } from "@/stores/auth"
import HistoryTimeline from "@/components/history/HistoryTimeline.vue"
import OpportunityActivities from "@/components/opportunity/OpportunityActivities.vue"

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const opportunity = ref(null)
const loading = ref(false)
const actionLoading = ref(false)
const error = ref("")
const historyVersion = ref(0)
const isFinal = computed(() => ["closed_won", "closed_lost"].includes(opportunity.value?.status))
const transitionMap = {
  new: [{ status: "qualification", label: "Qualifier", color: "primary", icon: "mdi-arrow-right", variant: "flat" }],
  qualification: [{ status: "proposal", label: "Créer la proposition", color: "primary", icon: "mdi-arrow-right", variant: "flat" }, { status: "closed_lost", label: "Marquer perdue", color: "error", icon: "mdi-close", variant: "tonal" }],
  proposal: [{ status: "negotiation", label: "Passer en négociation", color: "primary", icon: "mdi-arrow-right", variant: "flat" }, { status: "closed_lost", label: "Marquer perdue", color: "error", icon: "mdi-close", variant: "tonal" }],
  negotiation: [{ status: "closed_won", label: "Gagner et créer l'événement", color: "success", icon: "mdi-calendar-check-outline", variant: "flat", createEvent: true }, { status: "closed_lost", label: "Marquer perdue", color: "error", icon: "mdi-close", variant: "tonal" }],
}
const transitions = computed(() => transitionMap[opportunity.value?.status] ?? [])

async function loadOpportunity() {
  loading.value = true
  error.value = ""
  try { opportunity.value = await opportunityService.getById(route.params.id) }
  catch (err) { error.value = err.response?.data?.detail ?? "Impossible de charger l'opportunité" }
  finally { loading.value = false }
}

async function runAction(action) {
  actionLoading.value = true
  error.value = ""
  try { await action() }
  catch (err) { error.value = err.response?.data?.detail ?? "Impossible d'effectuer cette action" }
  finally { actionLoading.value = false }
}

function runTransition(transition) {
  return runAction(async () => {
    opportunity.value = await opportunityService.updateStatus(
      route.params.id,
      transition.status,
    )
    historyVersion.value += 1

    if (transition.createEvent) {
      await createEvent()
    }
  })
}

function createEvent() {
  return router.push({
    name: "EventCreate",
    query: {
      opportunityId: opportunity.value.id,
      companyId: opportunity.value.company_id,
      contactId: opportunity.value.contact_id,
      assignedUserId: opportunity.value.commercial_id,
      title: opportunity.value.title,
      source: "opportunity",
    },
  })
}
async function deleteOpportunity() {
  if (!window.confirm(`Supprimer l'opportunité ${opportunity.value.title} ?`)) return
  await runAction(async () => { await opportunityService.delete(route.params.id); await router.push({ name: "Opportunities" }) })
}
function goToList() { router.push({ name: "Opportunities" }) }
function goToEdit() { router.push({ name: "OpportunityEdit", params: { id: route.params.id } }) }
watch(() => route.params.id, (newId, oldId) => { if (newId && newId !== oldId) loadOpportunity() })
onMounted(loadOpportunity)
</script>
