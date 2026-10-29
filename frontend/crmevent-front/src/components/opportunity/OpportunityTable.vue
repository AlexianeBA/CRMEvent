<template>
  <DataTable ref="table" resource="opportunities" :columns="columns">
    <template #cell-status="{ value }"
      ><v-chip :color="statusColor(value)" size="small" variant="tonal">{{
        statusLabel(value)
      }}</v-chip></template
    >
    <template #actions="{ item }">
      <div class="action-buttons">
        <v-btn
          icon="mdi-eye-outline"
          variant="text"
          size="small"
          title="Voir l'opportunité"
          @click.stop="viewOpportunity(item)"
        />
        <v-btn
          v-if="auth.canManageCrm"
          icon="mdi-pencil-outline"
          variant="text"
          size="small"
          title="Modifier l'opportunité"
          :disabled="isFinal(item)"
          @click.stop="editOpportunity(item)"
        />
        <v-btn
          v-if="auth.canDeleteCrm"
          icon="mdi-delete-outline"
          variant="text"
          size="small"
          color="error"
          title="Supprimer l'opportunité"
          :disabled="isFinal(item)"
          @click.stop="deleteOpportunity(item)"
        />
      </div>
    </template>
  </DataTable>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import DataTable from '@/components/common/DataTable.vue'
import opportunityService from '@/services/opportunityService'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const table = ref(null)
const auth = useAuthStore()
const labels = {
  new: 'Nouvelle',
  qualification: 'Qualification',
  proposal: 'Proposition',
  negotiation: 'Négociation',
  closed_won: 'Gagnée',
  closed_lost: 'Perdue',
}
const colors = {
  new: 'blue-grey',
  qualification: 'blue',
  proposal: 'cyan',
  negotiation: 'orange',
  closed_won: 'green',
  closed_lost: 'red',
}
const columns = [
  { key: 'title', label: 'Titre' },
  {
    key: 'amount',
    label: 'Montant',
    formatter: (value) =>
      new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR' }).format(
        Number(value ?? 0),
      ),
  },
  { key: 'company', label: 'Entreprise', formatter: (value) => value?.name ?? '—' },
  { key: 'status', label: 'Statut' },
]

const statusLabel = (status) => labels[status] ?? status
const statusColor = (status) => colors[status] ?? 'grey'
const isFinal = (item) => ['closed_won', 'closed_lost'].includes(item.status)
const viewOpportunity = (item) => router.push({ name: 'OpportunityView', params: { id: item.id } })
const editOpportunity = (item) => router.push({ name: 'OpportunityEdit', params: { id: item.id } })

async function deleteOpportunity(item) {
  if (!window.confirm(`Supprimer l'opportunité ${item.title} ?`)) return
  try {
    await opportunityService.delete(item.id)
    table.value?.reload()
  } catch (error) {
    window.alert(error.response?.data?.detail ?? "Impossible de supprimer l'opportunité")
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
