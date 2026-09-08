<template>
  <header>
    <div>
      <h2>{{ pageTitle }}</h2>
      <p>Bienvenue sur CRM Event</p>
    </div>

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
import { computed, reactive, ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth"

defineOptions({ name: "DashboardHeader" })

const auth = useAuthStore()
const route = useRoute()
const router = useRouter()
const profileDialog = ref(false)
const passwordDialog = ref(false)
const passwordChanged = ref(false)
const passwordSaving = ref(false)
const passwordError = ref("")
const passwordFormRef = ref(null)
const showPasswords = ref(false)
const passwordForm = reactive({ currentPassword: "", newPassword: "", confirmPassword: "" })

const roleLabels = { admin: "Administrateur", manager: "Manager", commercial: "Commercial", comptable: "Comptable" }
const pageTitles = {
  companies: "Entreprises",
  contacts: "Contacts",
  opportunities: "Opportunités",
  events: "Événements",
  quotes: "Devis",
  invoices: "Factures",
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
</script>

<style scoped>
header { display: flex; justify-content: space-between; align-items: center; padding: 20px 30px; background: white; border-bottom: 1px solid #eee; }
header p { margin: 2px 0 0; color: #6b7280; }
.account-button { height: auto; padding: 6px 10px; text-transform: none; }
.account-summary { display: flex; flex-direction: column; align-items: flex-start; margin: 0 8px; }
.account-summary small { color: #6b7280; }
.profile-title { display: flex; align-items: center; gap: 14px; padding: 24px; }
.profile-title small { color: #6b7280; font-size: 0.85rem; font-weight: 400; }
.password-success { display: flex; flex-direction: column; align-items: center; gap: 12px; padding: 36px; text-align: center; }
.password-success p { color: #6b7280; }
@media (max-width: 700px) { .account-summary { display: none; } header { padding: 16px; } }
</style>
