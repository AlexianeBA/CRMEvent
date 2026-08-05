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
          title="Voir l'entreprise"
          @click.stop="viewCompany(item)"
        />

        <v-btn
          icon="mdi-pencil-outline"
          variant="text"
          size="small"
          title="Modifier l'entreprise"
          @click.stop="editCompany(item)"
        />

        <v-btn
          icon="mdi-delete-outline"
          variant="text"
          size="small"
          color="error"
          title="Supprimer l'entreprise"
          @click.stop="deleteCompany(item)"
        />
      </div>
    </template>
  </DataTable>
</template>

<script setup>
import { onMounted } from "vue"
import { useRouter } from "vue-router"

import { useCompanyStore } from "@/stores/company"
import DataTable from "@/components/common/DataTable.vue"

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
  console.log("Bouton voir :", company)

  if (!company?.id) {
    console.error("L'entreprise ne possède pas d'identifiant :", company)
    return
  }

  router.push({
    name: "CompanyView",
    params: {
      id: company.id,
    },
  })
}

function editCompany(company) {
  console.log("Bouton modifier :", company)

  if (!company?.id) {
    console.error("L'entreprise ne possède pas d'identifiant :", company)
    return
  }

  router.push({
    name: "CompanyEdit",
    params: {
      id: company.id,
    },
  })
}

async function deleteCompany(company) {
  if (!company?.id) {
    console.error("L'entreprise ne possède pas d'identifiant :", company)
    return
  }

  const confirmed = window.confirm(
    `Supprimer l'entreprise ${company.name} ?`,
  )

  if (!confirmed) {
    return
  }

  try {
    await store.deleteCompany(company.id)
  } catch (error) {
    console.error(
      "Erreur pendant la suppression de l'entreprise :",
      error,
    )
  }
}

onMounted(() => {
  store.loadCompanies()
})
</script>

<style scoped>
.action-buttons {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 4px;
}
</style>