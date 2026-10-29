<template>
  <DataTable ref="table" resource="companies" :columns="columns">
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
          v-if="auth.canManageCrm"
          icon="mdi-pencil-outline"
          variant="text"
          size="small"
          title="Modifier l'entreprise"
          @click.stop="editCompany(item)"
        />

        <v-btn
          v-if="auth.canDeleteCrm"
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
import { ref } from 'vue'
import { useRouter } from 'vue-router'

import companyService from '@/services/companyService'
import DataTable from '@/components/common/DataTable.vue'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const table = ref(null)
const auth = useAuthStore()

const columns = [
  {
    key: 'name',
    label: 'Nom',
  },
  {
    key: 'address',
    label: 'Adresse',
  },
  {
    key: 'city',
    label: 'Ville',
  },
]

function viewCompany(company) {
  console.log('Bouton voir :', company)

  if (!company?.id) {
    console.error("L'entreprise ne possède pas d'identifiant :", company)
    return
  }

  router.push({
    name: 'CompanyView',
    params: {
      id: company.id,
    },
  })
}

function editCompany(company) {
  console.log('Bouton modifier :', company)

  if (!company?.id) {
    console.error("L'entreprise ne possède pas d'identifiant :", company)
    return
  }

  router.push({
    name: 'CompanyEdit',
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

  const confirmed = window.confirm(`Supprimer l'entreprise ${company.name} ?`)

  if (!confirmed) {
    return
  }

  try {
    await companyService.delete(company.id)
    table.value?.reload()
  } catch (error) {
    console.error("Erreur pendant la suppression de l'entreprise :", error)
  }
}
</script>

<style scoped>
.action-buttons {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 4px;
}
</style>
