<template>
  <DashboardLayout>
    <section class="dashboard">
      <v-alert v-if="error" type="error" variant="tonal" closable @click:close="error = ''">{{ error }}</v-alert>
      <StatsCard :loading="loading" :stats="stats" />
      <div class="dashboard-grid">
        <div class="main-column">
          <UpcomingEvents :loading="loading" :events="events" />
          <TimelineCard :loading="loading" :opportunities="opportunities" />
        </div>
        <div class="side-column">
          <ProvidersCard :loading="loading" :quotes="quotes" :invoices="invoices" />
          <TasksCard :loading="loading" :events="events" :quotes="quotes" :invoices="invoices" />
        </div>
      </div>
    </section>
  </DashboardLayout>
</template>

<script setup>
import { computed, onMounted, ref } from "vue"
import DashboardLayout from "@/layouts/DashboardLayout.vue"
import StatsCard from "@/components/dashboard/StatsCard.vue"
import UpcomingEvents from "@/components/dashboard/UpcomingEvents.vue"
import TimelineCard from "@/components/dashboard/TimelineCard.vue"
import ProvidersCard from "@/components/dashboard/ProvidersCard.vue"
import TasksCard from "@/components/dashboard/TasksCard.vue"
import companyService from "@/services/companyService"
import contactService from "@/services/contactService"
import opportunityService from "@/services/opportunityService"
import eventService from "@/services/eventService"
import quoteService from "@/services/quotesService"
import invoiceService from "@/services/invoiceService"

defineOptions({ name: "DashboardPage" })

const loading = ref(false)
const error = ref("")
const companies = ref([])
const contacts = ref([])
const opportunities = ref([])
const events = ref([])
const quotes = ref([])
const invoices = ref([])

const stats = computed(() => [
  { label: "Entreprises", value: companies.value.length, icon: "mdi-domain", color: "indigo", route: "Companies" },
  { label: "Contacts", value: contacts.value.length, icon: "mdi-account-multiple-outline", color: "cyan", route: "Contacts" },
  { label: "Opportunités", value: opportunities.value.length, icon: "mdi-briefcase-outline", color: "orange", route: "Opportunities" },
  { label: "Événements", value: events.value.length, icon: "mdi-calendar-outline", color: "purple", route: "Events" },
  { label: "Devis", value: quotes.value.length, icon: "mdi-file-document-outline", color: "blue", route: "Quotes" },
  { label: "Factures", value: invoices.value.length, icon: "mdi-receipt-text-outline", color: "green", route: "Invoices" },
])

async function loadDashboard() {
  loading.value = true
  error.value = ""
  const requests = [
    [companies, companyService.getCompanies()],
    [contacts, contactService.getContacts()],
    [opportunities, opportunityService.getOpportunities()],
    [events, eventService.getEvents()],
    [quotes, quoteService.getQuotes()],
    [invoices, invoiceService.getInvoices()],
  ]
  const results = await Promise.allSettled(requests.map(([, request]) => request))
  results.forEach((result, index) => {
    if (result.status === "fulfilled") requests[index][0].value = result.value
  })
  if (results.some((result) => result.status === "rejected")) error.value = "Certaines données du tableau de bord n'ont pas pu être chargées"
  loading.value = false
}

onMounted(loadDashboard)
</script>

<style scoped>
.dashboard { display: flex; flex-direction: column; gap: 24px; }
.dashboard-grid { display: grid; grid-template-columns: minmax(0, 2fr) minmax(300px, 1fr); gap: 24px; }
.main-column, .side-column { display: flex; flex-direction: column; gap: 24px; }
@media (max-width: 1000px) { .dashboard-grid { grid-template-columns: 1fr; } }
</style>
