<template>
  <DataTable
    :items="store.contacts"
    :columns="columns"
    :search-fields="['last_name', 'first_name', 'phone_number', 'email']"
    :loading="store.loading"
  />
</template>

<script setup>
import { onMounted } from "vue"
import { useContactStore } from "@/stores/contact"
import DataTable from "@/components/DataTable.vue"


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
onMounted(() => {
  store.loadContacts()
})
</script>
