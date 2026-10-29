<template>
  <DashboardLayout>
    <div class="page-header">
      <div>
        <h1>Administration</h1>
        <p>Gestion des utilisateurs et de leurs rôles</p>
      </div>
      <v-btn color="primary" prepend-icon="mdi-account-plus" @click="createDialog = true">
        Nouvel utilisateur
      </v-btn>
    </div>

    <v-alert
      v-if="error"
      type="error"
      variant="tonal"
      closable
      class="mb-4"
      @click:close="error = ''"
    >
      {{ error }}
    </v-alert>
    <v-alert
      v-if="success"
      type="success"
      variant="tonal"
      closable
      class="mb-4"
      @click:close="success = ''"
    >
      {{ success }}
    </v-alert>

    <DataTable ref="table" resource="users" :columns="columns">
      <template #cell-role="{ item: user }">
        <v-select
          :model-value="user.role"
          :items="roles"
          item-title="label"
          item-value="value"
          density="compact"
          variant="outlined"
          hide-details
          :disabled="savingId === user.id"
          @update:model-value="updateRole(user, $event)"
        />
      </template>
      <template #cell-is_active="{ item: user }">
        <v-switch
          :model-value="Boolean(user.is_active)"
          color="success"
          hide-details
          :disabled="savingId === user.id"
          @update:model-value="updateActive(user, $event)"
        />
      </template>
      <template #actions="{ item: user }">
        <v-btn variant="text" prepend-icon="mdi-lock-reset" @click="openPasswordDialog(user)"
          >Mot de passe</v-btn
        >
      </template>
    </DataTable>

    <v-dialog v-model="createDialog" max-width="520">
      <v-card title="Nouvel utilisateur">
        <v-card-text>
          <v-text-field v-model="newUser.email" label="Email" type="email" variant="outlined" />
          <v-text-field
            v-model="newUser.password"
            label="Mot de passe"
            type="password"
            variant="outlined"
            hint="8 caractères minimum"
          />
          <v-select
            v-model="newUser.role"
            :items="roles"
            item-title="label"
            item-value="value"
            label="Rôle"
            variant="outlined"
          />
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="createDialog = false">Annuler</v-btn>
          <v-btn color="primary" :loading="dialogSaving" @click="createUser">Créer</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="passwordDialog" max-width="520">
      <v-card title="Réinitialiser le mot de passe">
        <v-card-text>
          <p class="mb-4">{{ selectedUser?.email }}</p>
          <v-text-field
            v-model="newPassword"
            label="Nouveau mot de passe"
            type="password"
            variant="outlined"
            hint="8 caractères minimum"
          />
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="passwordDialog = false">Annuler</v-btn>
          <v-btn color="primary" :loading="dialogSaving" @click="resetPassword">Enregistrer</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </DashboardLayout>
</template>

<script setup>
import { reactive, ref } from 'vue'
import DataTable from '@/components/common/DataTable.vue'
import DashboardLayout from '@/layouts/DashboardLayout.vue'
import adminService from '@/services/adminService'

const table = ref(null)
const columns = [
  { key: 'email', label: 'Email' },
  { key: 'role', label: 'Rôle' },
  { key: 'is_active', label: 'Compte actif' },
]
const savingId = ref(null)
const dialogSaving = ref(false)
const error = ref('')
const success = ref('')
const createDialog = ref(false)
const passwordDialog = ref(false)
const selectedUser = ref(null)
const newPassword = ref('')
const newUser = reactive({ email: '', password: '', role: 'commercial' })
const roles = [
  { label: 'Administrateur', value: 'admin' },
  { label: 'Manager', value: 'manager' },
  { label: 'Commercial', value: 'commercial' },
  { label: 'Comptable', value: 'comptable' },
]

const loadUsers = () => table.value?.reload()

async function saveUser(user, changes, message) {
  savingId.value = user.id
  error.value = ''
  try {
    const updated = await adminService.updateUser(user.id, changes)
    Object.assign(user, updated)
    loadUsers()
    success.value = message
  } catch (err) {
    error.value = err.response?.data?.detail ?? "Impossible de modifier l'utilisateur"
    await loadUsers()
  } finally {
    savingId.value = null
  }
}

function updateRole(user, role) {
  if (role === user.role) return
  saveUser(user, { role }, 'Rôle mis à jour')
}

function updateActive(user, isActive) {
  saveUser(user, { is_active: isActive }, isActive ? 'Compte activé' : 'Compte désactivé')
}

async function createUser() {
  if (!newUser.email.trim() || newUser.password.length < 8) {
    error.value = "Renseignez un email et un mot de passe d'au moins 8 caractères"
    return
  }
  dialogSaving.value = true
  try {
    await adminService.createUser({ ...newUser, email: newUser.email.trim() })
    Object.assign(newUser, { email: '', password: '', role: 'commercial' })
    createDialog.value = false
    success.value = 'Utilisateur créé'
    await loadUsers()
  } catch (err) {
    error.value = err.response?.data?.detail ?? "Impossible de créer l'utilisateur"
  } finally {
    dialogSaving.value = false
  }
}

function openPasswordDialog(user) {
  selectedUser.value = user
  newPassword.value = ''
  passwordDialog.value = true
}

async function resetPassword() {
  if (newPassword.value.length < 8) {
    error.value = 'Le mot de passe doit contenir au moins 8 caractères'
    return
  }
  dialogSaving.value = true
  try {
    await adminService.resetPassword(selectedUser.value.id, newPassword.value)
    passwordDialog.value = false
    success.value = 'Mot de passe réinitialisé'
  } catch (err) {
    error.value = err.response?.data?.detail ?? 'Impossible de réinitialiser le mot de passe'
  } finally {
    dialogSaving.value = false
  }
}
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}
.page-header p {
  color: #6b7280;
}
.state-message {
  padding: 30px;
  text-align: center;
  color: #6b7280;
}
th:nth-child(2) {
  width: 240px;
}
th:nth-child(3) {
  width: 140px;
}
</style>
