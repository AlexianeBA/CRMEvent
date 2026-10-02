<template>
  <header>
    <div class="page-identity">
      <h2>{{ pageTitle }}</h2>
      <p>Bienvenue sur CRM Event</p>
    </div>

    <v-menu v-model="searchMenu" location="bottom" :close-on-content-click="false" :open-on-click="false">
      <template #activator="{ props }">
        <v-text-field
          v-bind="props"
          v-model="searchQuery"
          class="global-search"
          density="compact"
          variant="solo-filled"
          flat
          hide-details
          clearable
          prepend-inner-icon="mdi-magnify"
          placeholder="Rechercher dans le CRM…"
          autocomplete="off"
          aria-label="Recherche globale"
          @focus="openSearch"
          @keydown.esc="searchMenu = false"
          @click:clear="resetSearch"
        />
      </template>
      <v-card width="560" max-width="calc(100vw - 24px)" class="search-results-card">
        <div v-if="searchLoading" class="search-state"><v-progress-circular indeterminate size="24" color="primary" /> Recherche…</div>
        <v-alert v-else-if="searchError" type="error" density="compact" variant="tonal" class="ma-3">{{ searchError }}</v-alert>
        <div v-else-if="searchQuery.trim().length < 2" class="search-state">Saisissez au moins 2 caractères</div>
        <div v-else-if="groupedResults.length === 0" class="search-state">Aucun résultat pour « {{ searchQuery }} »</div>
        <div v-else class="search-groups">
          <section v-for="group in groupedResults" :key="group.type" class="search-group">
            <div class="search-group-title"><v-icon :icon="group.icon" size="17" />{{ group.label }}</div>
            <button v-for="result in group.items" :key="`${result.type}-${result.id}`" type="button" class="search-result" @click="openSearchResult(result)">
              <v-icon :icon="group.icon" color="primary" size="20" />
              <span><strong>{{ result.title }}</strong><small v-if="result.subtitle">{{ result.subtitle }}</small></span>
              <v-icon icon="mdi-chevron-right" size="18" color="grey" />
            </button>
          </section>
        </div>
      </v-card>
    </v-menu>

    <div class="header-actions">
      <v-menu v-model="notificationMenu" location="bottom end" :close-on-content-click="false">
        <template #activator="{ props }">
          <v-btn v-bind="props" icon variant="text" title="Notifications">
            <v-badge :content="notifications.unreadCount" :model-value="notifications.unreadCount > 0" color="error">
              <v-icon icon="mdi-bell-outline" />
            </v-badge>
          </v-btn>
        </template>

        <v-card width="390" max-width="calc(100vw - 24px)" class="notification-menu">
          <div class="notification-header">
            <strong>Notifications</strong>
            <v-btn v-if="notifications.unreadCount" size="small" variant="text" @click="notifications.markAllAsRead()">Tout lire</v-btn>
          </div>
          <v-alert v-if="notifications.error" type="error" density="compact" variant="tonal" class="ma-3">{{ notifications.error }}</v-alert>
          <div v-if="notifications.loading && notifications.items.length === 0" class="notification-state">Chargement...</div>
          <div v-else-if="notifications.items.length === 0" class="notification-state">Aucune notification</div>
          <v-list v-else lines="three" class="notification-list">
            <v-list-item v-for="notification in notifications.items.slice(0, 8)" :key="notification.id" :class="{ unread: !notification.is_read }" @click="openNotification(notification)">
              <template #prepend>
                <v-avatar :color="severityColors[notification.severity]" variant="tonal" size="38">
                  <v-icon :icon="typeIcons[notification.type] ?? 'mdi-bell-outline'" size="small" />
                </v-avatar>
              </template>
              <v-list-item-title>{{ notification.title }}</v-list-item-title>
              <v-list-item-subtitle>{{ notification.message }}</v-list-item-subtitle>
              <small>{{ formatDate(notification.created_at) }}</small>
              <template #append>
                <v-btn icon="mdi-close" size="x-small" variant="text" title="Archiver" @click.stop="notifications.archive(notification)" />
              </template>
            </v-list-item>
          </v-list>
          <v-divider />
          <v-card-actions><v-btn block variant="text" @click="openNotificationCenter">Voir toutes les notifications</v-btn></v-card-actions>
        </v-card>
      </v-menu>

      <v-menu location="bottom end">
      <template #activator="{ props }">
        <v-btn v-bind="props" variant="text" class="account-button">
          <v-avatar color="primary" size="38">{{ initials }}</v-avatar>
          <div class="account-summary">
            <strong>{{ auth.user?.email }}</strong>
            <small>{{ roleLabel }}</small>
          </div>
          <v-icon icon="mdi-chevron-down" />
        </v-btn>
      </template>

      <v-list min-width="260">
        <v-list-item prepend-icon="mdi-account-circle-outline" title="Mon profil" @click="profileDialog = true" />
        <v-list-item prepend-icon="mdi-lock-reset" title="Changer mon mot de passe" @click="openPasswordDialog" />
        <v-list-item v-if="auth.isAdmin" prepend-icon="mdi-shield-account-outline" title="Administration" @click="goToAdmin" />
        <v-divider class="my-2" />
        <v-list-item prepend-icon="mdi-logout" title="Se déconnecter" base-color="error" @click="auth.logout()" />
      </v-list>
      </v-menu>
    </div>
  </header>

  <v-dialog v-model="profileDialog" max-width="500">
    <v-card>
      <v-card-title class="profile-title">
        <v-avatar color="primary" size="54">{{ initials }}</v-avatar>
        <div><div>Mon profil</div><small>{{ auth.user?.email }}</small></div>
      </v-card-title>
      <v-card-text>
        <v-list>
          <v-list-item prepend-icon="mdi-email-outline" title="Adresse email" :subtitle="auth.user?.email" />
          <v-list-item prepend-icon="mdi-badge-account-outline" title="Rôle" :subtitle="roleLabel" />
          <v-list-item prepend-icon="mdi-check-circle-outline" title="État du compte" :subtitle="auth.user?.is_active ? 'Actif' : 'Inactif'" />
        </v-list>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn variant="text" @click="profileDialog = false">Fermer</v-btn>
        <v-btn color="primary" variant="tonal" prepend-icon="mdi-lock-reset" @click="openPasswordFromProfile">Changer le mot de passe</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <v-dialog v-model="passwordDialog" max-width="520" persistent>
    <v-card title="Changer mon mot de passe">
      <template v-if="!passwordChanged">
        <v-card-text>
          <v-alert v-if="passwordError" type="error" variant="tonal" class="mb-4">{{ passwordError }}</v-alert>
          <v-form ref="passwordFormRef" @submit.prevent="submitPassword">
            <v-text-field v-model="passwordForm.currentPassword" label="Mot de passe actuel" :type="showPasswords ? 'text' : 'password'" variant="outlined" autocomplete="current-password" :rules="[rules.required]" />
            <v-text-field v-model="passwordForm.newPassword" label="Nouveau mot de passe" :type="showPasswords ? 'text' : 'password'" variant="outlined" autocomplete="new-password" hint="8 caractères minimum" :rules="[rules.required, rules.passwordLength]" />
            <v-text-field v-model="passwordForm.confirmPassword" label="Confirmer le nouveau mot de passe" :type="showPasswords ? 'text' : 'password'" variant="outlined" autocomplete="new-password" :rules="[rules.required, rules.passwordConfirmation]" />
            <v-checkbox v-model="showPasswords" label="Afficher les mots de passe" hide-details />
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" :disabled="passwordSaving" @click="passwordDialog = false">Annuler</v-btn>
          <v-btn color="primary" :loading="passwordSaving" @click="submitPassword">Enregistrer</v-btn>
        </v-card-actions>
      </template>
      <template v-else>
        <v-card-text class="password-success">
          <v-icon icon="mdi-check-circle" color="success" size="58" />
          <h3>Mot de passe modifié</h3>
          <p>Reconnectez-vous avec votre nouveau mot de passe.</p>
        </v-card-text>
        <v-card-actions><v-spacer /><v-btn color="primary" @click="auth.logout()">Se reconnecter</v-btn></v-card-actions>
      </template>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, reactive, ref, watch } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth"
import { useNotificationStore } from "@/stores/notifications"
import searchService from "@/services/searchService"

defineOptions({ name: "DashboardHeader" })

const auth = useAuthStore()
const notifications = useNotificationStore()
const route = useRoute()
const router = useRouter()
const profileDialog = ref(false)
const passwordDialog = ref(false)
const passwordChanged = ref(false)
const passwordSaving = ref(false)
const passwordError = ref("")
const passwordFormRef = ref(null)
const showPasswords = ref(false)
const notificationMenu = ref(false)
const searchMenu = ref(false)
const searchQuery = ref("")
const searchResults = ref([])
const searchLoading = ref(false)
const searchError = ref("")
let notificationTimer
let searchTimer
let searchRequestId = 0
const passwordForm = reactive({ currentPassword: "", newPassword: "", confirmPassword: "" })

const roleLabels = { admin: "Administrateur", manager: "Manager", commercial: "Commercial", comptable: "Comptable" }
const pageTitles = {
  companies: "Entreprises",
  contacts: "Contacts",
  opportunities: "Opportunités",
  events: "Événements",
  quotes: "Devis",
  invoices: "Factures",
  tasks: "Tâches",
  admin: "Administration",
}
const pageTitle = computed(() => {
  const section = route.path.split("/")[1]
  return pageTitles[section] ?? "Tableau de bord"
})
const roleLabel = computed(() => roleLabels[auth.user?.role] ?? "Utilisateur")
const initials = computed(() => (auth.user?.email ?? "U").slice(0, 2).toUpperCase())
const rules = {
  required: (value) => Boolean(value) || "Ce champ est obligatoire",
  passwordLength: (value) => String(value ?? "").length >= 8 || "8 caractères minimum",
  passwordConfirmation: (value) => value === passwordForm.newPassword || "Les mots de passe ne correspondent pas",
}
const severityColors = { info: "primary", warning: "warning", error: "error" }
const typeIcons = {
  event_upcoming: "mdi-calendar-clock",
  opportunity_inactive: "mdi-briefcase-clock-outline",
  quote_unanswered: "mdi-file-clock-outline",
  invoice_due: "mdi-receipt-clock-outline",
  invoice_overdue: "mdi-alert-circle-outline",
  task_assigned: "mdi-clipboard-check-outline",
  task_due: "mdi-clipboard-clock-outline",
}
const searchTypes = {
  company: { label: "Entreprises", icon: "mdi-domain" },
  contact: { label: "Contacts", icon: "mdi-account-outline" },
  opportunity: { label: "Opportunités", icon: "mdi-briefcase-outline" },
  event: { label: "Événements", icon: "mdi-calendar-outline" },
  quote: { label: "Devis", icon: "mdi-file-document-outline" },
  invoice: { label: "Factures", icon: "mdi-receipt-text-outline" },
}
const groupedResults = computed(() => Object.entries(searchTypes).map(([type, config]) => ({
  type,
  ...config,
  items: searchResults.value.filter((item) => item.type === type),
})).filter((group) => group.items.length))

watch(searchQuery, (value) => {
  window.clearTimeout(searchTimer)
  searchError.value = ""
  const query = value.trim()
  if (query.length < 2) {
    searchResults.value = []
    searchLoading.value = false
    searchMenu.value = Boolean(query)
    return
  }
  searchMenu.value = true
  searchLoading.value = true
  const requestId = ++searchRequestId
  searchTimer = window.setTimeout(async () => {
    try {
      const results = await searchService.search(query)
      if (requestId === searchRequestId) searchResults.value = results
    } catch {
      if (requestId === searchRequestId) searchError.value = "Impossible d'effectuer la recherche"
    } finally {
      if (requestId === searchRequestId) searchLoading.value = false
    }
  }, 300)
})

function resetPasswordForm() {
  Object.assign(passwordForm, { currentPassword: "", newPassword: "", confirmPassword: "" })
  passwordError.value = ""
  passwordChanged.value = false
  showPasswords.value = false
  passwordFormRef.value?.resetValidation()
}

function openPasswordDialog() {
  resetPasswordForm()
  passwordDialog.value = true
}

function openPasswordFromProfile() {
  profileDialog.value = false
  openPasswordDialog()
}

async function submitPassword() {
  const validation = await passwordFormRef.value?.validate()
  if (!validation?.valid) return
  passwordSaving.value = true
  passwordError.value = ""
  try {
    await auth.changePassword(passwordForm.currentPassword, passwordForm.newPassword)
    passwordChanged.value = true
  } catch (error) {
    passwordError.value = error.response?.data?.detail ?? "Impossible de modifier le mot de passe"
  } finally {
    passwordSaving.value = false
  }
}

function goToAdmin() {
  router.push({ name: "AdminUsers" })
}

function openSearch() {
  if (searchQuery.value.trim()) searchMenu.value = true
}

function resetSearch() {
  searchRequestId += 1
  window.clearTimeout(searchTimer)
  searchQuery.value = ""
  searchResults.value = []
  searchLoading.value = false
  searchError.value = ""
  searchMenu.value = false
}

async function openSearchResult(result) {
  searchMenu.value = false
  await router.push(result.url)
  resetSearch()
}

async function openNotification(notification) {
  await notifications.markAsRead(notification)
  notificationMenu.value = false
  if (notification.target_url) await router.push(notification.target_url)
}

function openNotificationCenter() {
  notificationMenu.value = false
  router.push({ name: "Notifications" })
}

function formatDate(value) {
  return new Intl.DateTimeFormat("fr-FR", { dateStyle: "short", timeStyle: "short" }).format(new Date(value))
}

onMounted(() => {
  notifications.refresh({ synchronize: true })
  notificationTimer = window.setInterval(() => notifications.refresh({ synchronize: true }), 60_000)
})
onBeforeUnmount(() => {
  window.clearInterval(notificationTimer)
  window.clearTimeout(searchTimer)
})
</script>

<style scoped>
header { display: flex; justify-content: space-between; align-items: center; gap: 24px; padding: 20px 30px; background: white; border-bottom: 1px solid #eee; }
header p { margin: 2px 0 0; color: #6b7280; }
.page-identity { flex: 0 0 auto; min-width: 190px; }
.global-search { flex: 0 1 520px; max-width: 520px; }
.search-results-card { overflow: hidden; }
.search-state { display: flex; align-items: center; justify-content: center; gap: 10px; min-height: 90px; padding: 24px; color: #6b7280; }
.search-groups { max-height: min(620px, calc(100vh - 120px)); overflow-y: auto; padding: 8px 0; }
.search-group + .search-group { border-top: 1px solid #eef2f7; }
.search-group-title { display: flex; align-items: center; gap: 7px; padding: 10px 16px 5px; color: #64748b; font-size: 12px; font-weight: 700; letter-spacing: .04em; text-transform: uppercase; }
.search-result { display: grid; grid-template-columns: 24px minmax(0, 1fr) 20px; align-items: center; gap: 10px; width: 100%; padding: 10px 16px; border: 0; background: transparent; color: #111827; text-align: left; cursor: pointer; }
.search-result:hover { background: #f5f7ff; }
.search-result span, .search-result strong, .search-result small { display: block; min-width: 0; }
.search-result strong, .search-result small { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.search-result small { margin-top: 2px; color: #6b7280; }
.header-actions { display: flex; align-items: center; gap: 4px; }
.account-button { height: auto; padding: 6px 10px; text-transform: none; }
.account-summary { display: flex; flex-direction: column; align-items: flex-start; margin: 0 8px; }
.account-summary small { color: #6b7280; }
.profile-title { display: flex; align-items: center; gap: 14px; padding: 24px; }
.profile-title small { color: #6b7280; font-size: 0.85rem; font-weight: 400; }
.password-success { display: flex; flex-direction: column; align-items: center; gap: 12px; padding: 36px; text-align: center; }
.password-success p { color: #6b7280; }
.notification-header { display: flex; align-items: center; justify-content: space-between; padding: 14px 16px 8px; }
.notification-list { max-height: 480px; overflow-y: auto; }
.notification-list .unread { background: #eff6ff; }
.notification-list small { color: #6b7280; }
.notification-state { padding: 32px 16px; color: #6b7280; text-align: center; }
@media (max-width: 950px) { .page-identity p { display: none; } .page-identity { min-width: auto; } }
@media (max-width: 700px) { .account-summary { display: none; } header { flex-wrap: wrap; padding: 16px; gap: 12px; } .global-search { order: 3; flex-basis: 100%; max-width: none; } }
</style>
