<template>
  <DashboardLayout>
    <div class="page-header">
      <div><h1>Opportunités</h1><p>Gestion du pipeline commercial</p></div>
      <v-btn color="primary" prepend-icon="mdi-plus" @click="goToCreate">Nouvelle opportunité</v-btn>
    </div>
    <OpportunityTable />
  </DashboardLayout>
</template>

<script setup>
import { useRouter } from "vue-router"
import DashboardLayout from "@/layouts/DashboardLayout.vue"
import OpportunityTable from "@/components/opportunity/OpportunityTable.vue"
const router = useRouter()
function goToCreate() { router.push({ name: "OpportunityCreate" }) }
</script>

<style scoped>
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
</style>
