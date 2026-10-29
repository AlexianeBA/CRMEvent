<template>
  <DashboardLayout>
    <div class="page-header">
      <div>
        <h1>Événements</h1>
        <p>Gestion des événements</p>
      </div>

      <div class="page-actions">
        <v-btn v-if="auth.canManageCrm" color="primary" prepend-icon="mdi-plus" @click="goToCreate"
          >Nouvel événement</v-btn
        >
      </div>
    </div>

    <EventTable />
  </DashboardLayout>
</template>

<script setup>
import DashboardLayout from '@/layouts/DashboardLayout.vue'
import EventTable from '@/components/event/EventTable.vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { eventService } from '@/services/eventService'

const router = useRouter()
const auth = useAuthStore()

function goToCreate() {
  router.push({
    name: 'EventCreate',
  })
}
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}
.page-actions {
  display: flex;
  gap: 10px;
}

.btn-primary {
  background: #3b82f6;
  color: white;
  padding: 12px 20px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}
</style>
