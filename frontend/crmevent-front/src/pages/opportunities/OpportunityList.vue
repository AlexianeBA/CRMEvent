<template>
  <DashboardLayout>
    <div class="page-header">
      <div><h1>Opportunités</h1><p>Gestion de l'opportunité commerciale</p></div>
      <v-btn v-if="auth.canManageCrm" color="primary" prepend-icon="mdi-plus" @click="goToCreate">Nouvelle opportunité</v-btn>
    </div>
    <OpportunityTable />
  </DashboardLayout>
</template>

<script setup>
import { useRouter } from "vue-router"
import DashboardLayout from "@/layouts/DashboardLayout.vue"
import OpportunityTable from "@/components/opportunity/OpportunityTable.vue"
import { useAuthStore } from "@/stores/auth"
const router = useRouter()
const auth = useAuthStore()
function goToCreate() { router.push({ name: "OpportunityCreate" }) }
</script>

<style scoped>
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
</style>
