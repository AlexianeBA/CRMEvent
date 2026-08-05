<template>
  <DataTable
    :items="store.contacts"
    :columns="columns"
    :search-fields="['last_name', 'first_name', 'phone_number', 'email']"
    :loading="store.loading"
  >
  <template #actions="{ item }">
      <div class="action-buttons">
        <v-btn
          icon="mdi-eye-outline"
          variant="text"
          size="small"
          @click="viewContact(item)"
        />

        <v-btn
          icon="mdi-pencil-outline"
          variant="text"
          size="small"
          @click="editContact(item)"
        />

        <v-btn
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
import { onMounted } from "vue"
import { useRouter } from "vue-router"
import { useContactStore } from "@/stores/contact"
import DataTable from "@/components/common/DataTable.vue"


const router = useRouter()
const store = useContactStore()

const columns = [
  {
    key: "last_name",
    label: "Nom",
  },
  {
    key: "first_name",
    label: "Prénom",
  },
  {
    key: "phone_number",
    label: "Téléphone",
  },
  {
    key: "email",
    label: "Email",
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

  await store.deleteContact(contact.id)
}

onMounted(() => {
  store.loadContacts()
})
</script>
