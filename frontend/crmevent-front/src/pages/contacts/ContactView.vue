<template>
  <DashboardLayout>
    <DetailPage
      :title="contact ? `${contact.first_name} ${contact.last_name}` : 'Détail du contact'"
      breadcrumb="Contacts / Détail"
      :loading="loading"
      :error="error"
      :show-edit="auth.canManageCrm"
      @back="goToList"
      @edit="goToEdit"
    >
      <ContactDetails
        v-if="contact"
        :contact="contact"
      />
      <HistoryTimeline v-if="contact" entity-type="contact" :entity-id="contact.id" />
    </DetailPage>
  </DashboardLayout>
</template>

<script setup>
import { onMounted, ref, watch } from "vue"
import { useRoute, useRouter } from "vue-router"

import DashboardLayout from "@/layouts/DashboardLayout.vue"
import DetailPage from "@/components/common/DetailPage.vue"
import ContactDetails from "@/components/contact/ContactDetails.vue"
import { contactService } from "@/services/contactService"
import { useAuthStore } from "@/stores/auth"
import HistoryTimeline from "@/components/history/HistoryTimeline.vue"

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const contact = ref(null)
const loading = ref(false)
const error = ref("")

async function loadContact() {
  const contactId = route.params.id

  if (!contactId) {
    error.value = "L'identifiant du contact est manquant"
    return
  }

  loading.value = true
  error.value = ""
  contact.value = null

  try {
    contact.value = await contactService.getById(contactId)
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

function goToList() {
  router.push({
    name: "Contacts",
  })
}

function goToEdit() {
  router.push({
    name: "ContactEdit",
    params: {
      id: route.params.id,
    },
  })
}

watch(
  () => route.params.id,
  (newId, oldId) => {
    if (newId && newId !== oldId) {
      loadContact()
    }
  },
)

onMounted(loadContact)
</script>
