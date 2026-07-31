<template>
  <DataTable
    :items="store.companies"
    :columns="columns"
    :search-fields="['name', 'address', 'city']"
    :loading="store.loading"
  >
    <template #actions="{ item }">
      <div class="action-buttons">
        <v-btn
          icon="mdi-eye-outline"
          variant="text"
          size="small"
          @click="viewCompany(item)"
        />

        <v-btn
          icon="mdi-pencil-outline"
          variant="text"
          size="small"
          @click="editCompany(item)"
        />

        <v-btn
          icon="mdi-delete-outline"
          variant="text"
          size="small"
          color="error"
          @click="deleteCompany(item)"
        />
      </div>
    </template>
  </DataTable>
</template>

<script setup>
import { onMounted } from "vue"
import { useRouter } from "vue-router"
import { useCompanyStore } from "@/stores/company"
import DataTable from "@/components/DataTable.vue"

const router = useRouter()
const store = useCompanyStore()

const columns = [
  {
    key: "name",
    label: "Nom",
  },
  {
    key: "address",
    label: "Adresse",
  },
  {
    key: "city",
    label: "Ville",
  },
]

function viewCompany(company) {
  router.push(`/companies/${company.id}`)
}

function editCompany(company) {
  router.push(`/companies/${company.id}/edit`)
}

async function deleteCompany(company) {
  const confirmed = window.confirm(
    `Supprimer l'entreprise ${company.name} ?`,
  )

  if (!confirmed) {
    return
  }

  await store.deleteCompany(company.id)
}

onMounted(() => {
  store.loadCompanies()
})
</script>

<style scoped>
.action-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 4px;
}
</style>