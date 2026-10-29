<template>
  <DataTable ref="table" resource="contacts" :columns="columns">
    <template #actions="{ item }">
      <div class="action-buttons">
        <v-btn icon="mdi-eye-outline" variant="text" size="small" @click="viewContact(item)" />

        <v-btn
          v-if="auth.canManageCrm"
          icon="mdi-pencil-outline"
          variant="text"
          size="small"
          @click="editContact(item)"
        />

        <v-btn
          v-if="auth.canDeleteCrm"
          icon="mdi-delete-outline"
          variant="text"
          size="small"
          color="error"
          @click="deleteContact(item)"
        />
      </div>
    </template>
  </DataTable>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import contactService from '@/services/contactService'
import DataTable from '@/components/common/DataTable.vue'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const table = ref(null)
const auth = useAuthStore()

const columns = [
  {
    key: 'last_name',
    label: 'Nom',
  },
  {
    key: 'first_name',
    label: 'Prénom',
  },
  {
    key: 'phone_number',
    label: 'Téléphone',
  },
  {
    key: 'email',
    label: 'Email',
  },
]

function viewContact(contact) {
  router.push(`/contacts/${contact.id}`)
}
function editContact(contact) {
  router.push(`/contacts/${contact.id}/edit`)
}
async function deleteContact(contact) {
  const confirmed = window.confirm(
    `Supprimer le contact ${contact.first_name} ${contact.last_name} ?`,
  )

  if (!confirmed) {
    return
  }

  await contactService.delete(contact.id)
  table.value?.reload()
}
</script>
