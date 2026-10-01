<template>
  <DashboardLayout>
    <section class="dashboard">
      <div class="dashboard-heading">
        <div><p class="eyebrow">{{ roleLabel }}</p><h1>{{ dashboardTitle }}</h1></div>
        <v-chip color="primary" variant="tonal" prepend-icon="mdi-account-circle-outline">{{ auth.user?.email }}</v-chip>
      </div>

      <v-alert v-if="error" type="warning" variant="tonal" closable @click:close="error = ''">{{ error }}</v-alert>
      <StatsCard :loading="loading" :stats="stats" />

      <div v-if="role === 'commercial'" class="dashboard-grid">
        <div class="main-column">
          <UpcomingEvents :loading="loading" :events="events" />
          <TimelineCard :loading="loading" :opportunities="opportunities" />
        </div>
        <div class="side-column">
          <section class="card">
            <div class="card-header"><div><h3>Devis à relancer</h3><p>Envoyés en attente de réponse</p></div><v-icon icon="mdi-file-clock-outline" color="primary" /></div>
            <v-skeleton-loader v-if="loading" type="list-item-three-line" />
            <div v-else-if="quotesToFollowUp.length" class="dashboard-list">
              <router-link v-for="item in quotesToFollowUp" :key="item.id" :to="{ name: 'QuoteView', params: { id: item.id } }" class="dashboard-list-row">
                <div><strong>{{ item.title }}</strong><span>{{ item.subtitle }}</span></div><strong>{{ item.value }}</strong>
              </router-link>
            </div>
            <p v-else class="empty-state">Aucun devis à relancer</p>
          </section>
        </div>
      </div>

      <div v-else-if="role === 'manager'" class="dashboard-grid">
        <div class="main-column"><TimelineCard :loading="loading" :opportunities="opportunities" /></div>
        <div class="side-column">
          <section class="card">
            <div class="card-header"><div><h3>Performance de l'équipe</h3><p>Portefeuille et opportunités gagnées</p></div><v-icon icon="mdi-account-group-outline" color="primary" /></div>
            <v-skeleton-loader v-if="loading" type="table-row-divider@4" />
            <div v-else-if="teamPerformance.length" class="team-list">
              <div v-for="member in teamPerformance" :key="member.id" class="team-row">
                <div><strong>{{ member.email }}</strong><span>{{ member.total }} opportunité(s), {{ member.won }} gagnée(s)</span></div>
                <strong>{{ formatCurrency(member.pipeline) }}</strong>
              </div>
            </div>
            <p v-else class="empty-state">Aucun commercial actif</p>
          </section>
        </div>
      </div>

      <div v-else-if="role === 'comptable'" class="dashboard-grid">
        <div class="main-column">
          <section class="card">
            <div class="card-header"><div><h3>Échéances à surveiller</h3><p>Factures impayées classées par date</p></div><v-icon icon="mdi-calendar-alert-outline" color="primary" /></div>
            <v-skeleton-loader v-if="loading" type="table-row-divider@4" />
            <div v-else-if="invoiceDeadlines.length" class="dashboard-list">
              <router-link v-for="item in invoiceDeadlines" :key="item.id" :to="{ name: 'InvoiceView', params: { id: item.id } }" :class="['dashboard-list-row', { danger: item.danger }]">
                <div><strong>{{ item.title }}</strong><span>{{ item.subtitle }}</span></div><strong>{{ item.value }}</strong>
              </router-link>
            </div>
            <p v-else class="empty-state">Aucune échéance en attente</p>
          </section>
        </div>
        <div class="side-column"><ProvidersCard :loading="loading" :quotes="[]" :invoices="invoices" :show-quotes="false" /></div>
      </div>

      <div v-else class="dashboard-grid">
        <div class="main-column">
          <TimelineCard :loading="loading" :opportunities="opportunities" />
          <UpcomingEvents :loading="loading" :events="events" />
        </div>
        <div class="side-column">
          <section class="card">
            <div class="card-header"><div><h3>Comptes désactivés</h3><p>Utilisateurs sans accès à l'application</p></div><v-icon icon="mdi-account-off-outline" color="primary" /></div>
            <v-skeleton-loader v-if="loading" type="list-item@3" />
            <div v-else-if="disabledUsers.length" class="disabled-list">
              <div v-for="user in disabledUsers" :key="user.id"><span>{{ user.email }}</span><v-chip size="x-small" color="error" variant="tonal">{{ roleName(user.role) }}</v-chip></div>
            </div>
            <p v-else class="empty-state">Aucun compte désactivé</p>
            <v-btn class="mt-4" block color="primary" variant="tonal" :to="{ name: 'AdminUsers' }">Gérer les utilisateurs</v-btn>
          </section>
          <ProvidersCard :loading="loading" :quotes="quotes" :invoices="invoices" />
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
import companyService from "@/services/companyService"
import contactService from "@/services/contactService"
import opportunityService from "@/services/opportunityService"
import eventService from "@/services/eventService"
import quoteService from "@/services/quotesService"
import invoiceService from "@/services/invoiceService"
import userService from "@/services/userService"
import { useAuthStore } from "@/stores/auth"

defineOptions({ name: "DashboardPage" })

const auth = useAuthStore()
const loading = ref(false)
const error = ref("")
const companies = ref([])
const contacts = ref([])
const opportunities = ref([])
const events = ref([])
const quotes = ref([])
const invoices = ref([])
const users = ref([])

const role = computed(() => auth.user?.role ?? "commercial")
const roleLabel = computed(() => roleName(role.value))
const dashboardTitle = computed(() => ({ commercial: "Mon activité commerciale", manager: "Performance de l'équipe", comptable: "Suivi de la facturation", admin: "Vue globale de l'activité" }[role.value] ?? "Tableau de bord"))
const openOpportunities = computed(() => opportunities.value.filter((item) => !["closed_won", "closed_lost"].includes(item.status)))
const wonOpportunities = computed(() => opportunities.value.filter((item) => item.status === "closed_won"))
const upcomingEvents = computed(() => events.value.filter((item) => {
  const date = parseBusinessDate(item.date)
  return date && date >= startOfToday() && !["held", "canceled", "locked"].includes(item.status)
}))
const quotesToFollowUp = computed(() => quotes.value.filter((item) => item.status === "sent").map((item) => ({ id: item.id, title: item.number ? `${item.number} · ${item.title}` : item.title, subtitle: item.company?.name ?? "Entreprise non renseignée", value: formatCurrency(item.total_amount) })))
const overdueInvoices = computed(() => invoices.value.filter(isOverdue))
const paidInvoices = computed(() => invoices.value.filter((item) => item.status === "paid"))
const dueInvoices = computed(() => invoices.value.filter((item) => !["paid", "canceled"].includes(item.status)))
const outstandingAmount = computed(() => dueInvoices.value.reduce((sum, item) => sum + Number(item.balance_remaining ?? item.total_incl_tax ?? item.total_amount ?? 0), 0))
const disabledUsers = computed(() => users.value.filter((user) => !Boolean(user.is_active)))

const invoiceDeadlines = computed(() => [...dueInvoices.value].sort((a, b) => new Date(a.due_date) - new Date(b.due_date)).map((item) => ({
  id: item.id,
  title: `${item.number} · ${item.company?.name ?? item.title}`,
  subtitle: `${isOverdue(item) ? "En retard depuis le" : "Échéance le"} ${formatDate(item.due_date)}`,
  value: formatCurrency(item.balance_remaining ?? item.total_incl_tax ?? item.total_amount),
  danger: isOverdue(item),
})))

const teamPerformance = computed(() => users.value.filter((user) => user.role === "commercial" && Boolean(user.is_active)).map((user) => {
  const items = opportunities.value.filter((item) => item.commercial_id === user.id)
  return { id: user.id, email: user.email, total: items.length, won: items.filter((item) => item.status === "closed_won").length, pipeline: items.filter((item) => !["closed_won", "closed_lost"].includes(item.status)).reduce((sum, item) => sum + Number(item.amount ?? 0), 0) }
}).sort((a, b) => b.pipeline - a.pipeline))

const stats = computed(() => {
  if (role.value === "commercial") return [
    stat("Mes opportunités", opportunities.value.length, "mdi-briefcase-outline", "orange", "Opportunities"),
    stat("Valeur du portefeuille", formatCurrency(sumAmounts(openOpportunities.value)), "mdi-chart-line", "indigo", "Opportunities"),
    stat("Événements à venir", upcomingEvents.value.length, "mdi-calendar-clock", "purple", "Events"),
    stat("Devis à relancer", quotesToFollowUp.value.length, "mdi-file-clock-outline", "blue", "Quotes"),
  ]
  if (role.value === "manager") {
    const conversion = opportunities.value.length ? Math.round((wonOpportunities.value.length / opportunities.value.length) * 100) : 0
    return [
      stat("Valeur du pipeline", formatCurrency(sumAmounts(openOpportunities.value)), "mdi-chart-areaspline", "indigo", "Opportunities"),
      stat("Opportunités ouvertes", openOpportunities.value.length, "mdi-briefcase-clock-outline", "orange", "Opportunities"),
      stat("Affaires gagnées", wonOpportunities.value.length, "mdi-trophy-outline", "green", "Opportunities"),
      stat("Taux de transformation", `${conversion} %`, "mdi-percent-outline", "cyan", "Opportunities"),
    ]
  }
  if (role.value === "comptable") return [
    stat("Factures dues", dueInvoices.value.length, "mdi-receipt-clock-outline", "orange", "Invoices"),
    stat("Montant à encaisser", formatCurrency(outstandingAmount.value), "mdi-cash-clock", "indigo", "Invoices"),
    stat("Factures payées", paidInvoices.value.length, "mdi-check-decagram-outline", "green", "Invoices"),
    stat("Factures en retard", overdueInvoices.value.length, "mdi-alert-circle-outline", "red", "Invoices"),
  ]
  return [
    stat("Entreprises", companies.value.length, "mdi-domain", "indigo", "Companies"), stat("Contacts", contacts.value.length, "mdi-account-multiple-outline", "cyan", "Contacts"),
    stat("Opportunités", opportunities.value.length, "mdi-briefcase-outline", "orange", "Opportunities"), stat("Événements", events.value.length, "mdi-calendar-outline", "purple", "Events"),
    stat("Utilisateurs actifs", users.value.length - disabledUsers.value.length, "mdi-account-check-outline", "green", "AdminUsers"), stat("Comptes désactivés", disabledUsers.value.length, "mdi-account-off-outline", "red", "AdminUsers"),
  ]
})

function stat(label, value, icon, color, route) { return { label, value, icon, color, route } }
function sumAmounts(items) { return items.reduce((sum, item) => sum + Number(item.amount ?? 0), 0) }
function startOfToday() { const date = new Date(); date.setHours(0, 0, 0, 0); return date }
function parseBusinessDate(value) {
  if (!value) return null
  const parts = String(value).split("-")
  const date = parts[0]?.length === 2 ? new Date(`${parts[2]}-${parts[1]}-${parts[0]}T00:00:00`) : new Date(value)
  return Number.isNaN(date.getTime()) ? null : date
}
function isOverdue(item) { return item.status === "overdue" || (!["paid", "canceled"].includes(item.status) && new Date(item.due_date) < startOfToday()) }
function formatCurrency(value) { return new Intl.NumberFormat("fr-FR", { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(Number(value ?? 0)) }
function formatDate(value) { return value ? new Intl.DateTimeFormat("fr-FR").format(new Date(value)) : "—" }
function roleName(value) { return ({ admin: "Administrateur", manager: "Manager", commercial: "Commercial", comptable: "Comptable" })[value] ?? value }

async function loadInto(target, promise) {
  try { target.value = await promise } catch { error.value = "Certaines données du tableau de bord n'ont pas pu être chargées" }
}

async function loadDashboard() {
  loading.value = true
  error.value = ""
  const userId = auth.user?.id
  let requests = []
  if (role.value === "commercial") requests = [loadInto(opportunities, opportunityService.getOpportunities({ commercial_id: userId })), loadInto(events, eventService.getEvents({ assigned_user_id: userId })), loadInto(quotes, quoteService.getQuotes({ assigned_user_id: userId }))]
  else if (role.value === "manager") requests = [loadInto(opportunities, opportunityService.getOpportunities()), loadInto(users, userService.getUsers())]
  else if (role.value === "comptable") requests = [loadInto(invoices, invoiceService.getInvoices())]
  else requests = [loadInto(companies, companyService.getCompanies()), loadInto(contacts, contactService.getContacts()), loadInto(opportunities, opportunityService.getOpportunities()), loadInto(events, eventService.getEvents()), loadInto(quotes, quoteService.getQuotes()), loadInto(invoices, invoiceService.getInvoices()), loadInto(users, userService.getAllUsers())]
  await Promise.all(requests)
  loading.value = false
}

onMounted(loadDashboard)
</script>

<style scoped>
.dashboard { display: flex; flex-direction: column; gap: 24px; }.dashboard-heading { display: flex; align-items: center; justify-content: space-between; gap: 16px; }.dashboard-heading h1 { margin: 2px 0 0; color: #0f172a; font-size: clamp(24px, 3vw, 32px); }.eyebrow { margin: 0; color: #4f46e5; font-size: 12px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; }
.dashboard-grid { display: grid; grid-template-columns: minmax(0, 2fr) minmax(300px, 1fr); gap: 24px; }.main-column, .side-column { display: flex; flex-direction: column; gap: 24px; min-width: 0; }.card { padding: 22px; border-radius: 14px; background: white; box-shadow: 0 1px 3px rgb(15 23 42 / 8%); }.card-header { display: flex; align-items: flex-start; justify-content: space-between; gap: 16px; margin-bottom: 18px; }.card-header h3, .card-header p { margin: 0; }.card-header p { margin-top: 4px; color: #64748b; font-size: 13px; }
.dashboard-list, .team-list, .disabled-list { display: flex; flex-direction: column; }.dashboard-list-row, .team-row, .disabled-list > div { display: flex; align-items: center; justify-content: space-between; gap: 14px; padding: 13px 0; border-bottom: 1px solid #eef2f7; }.dashboard-list-row { color: #0f172a; text-decoration: none; }.dashboard-list-row:hover { color: #4f46e5; }.dashboard-list-row div, .team-row div { min-width: 0; }.dashboard-list-row span, .team-row span { display: block; overflow: hidden; margin-top: 3px; color: #64748b; font-size: 12px; text-overflow: ellipsis; white-space: nowrap; }.dashboard-list-row.danger > strong, .dashboard-list-row.danger div > span { color: #dc2626; }.team-row > strong { color: #4f46e5; white-space: nowrap; }.empty-state { margin: 28px 0; color: #94a3b8; text-align: center; }
@media (max-width: 1000px) { .dashboard-grid { grid-template-columns: 1fr; } } @media (max-width: 600px) { .dashboard-heading { align-items: flex-start; flex-direction: column; } }
</style>
