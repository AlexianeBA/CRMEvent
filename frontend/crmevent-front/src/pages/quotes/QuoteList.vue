<template>
  <DashboardLayout>

    <div class="page-header">
      <div>
        <h1>Devis</h1>
        <p>Gestion des devis clients</p>
      </div>

      <v-btn
        color="primary"
        prepend-icon="mdi-plus"
        @click="goToCreate"
      >
        Nouveau devis
      </v-btn>
    </div>

    <QuoteTable />

  </DashboardLayout>
</template>

<script setup>
import { useRouter } from "vue-router"
import DashboardLayout from "@/layouts/DashboardLayout.vue"
import QuoteTable from "@/components/quotes/QuoteTable.vue"

const router = useRouter()

function goToCreate() {
  router.push({
    name: "QuoteCreate",
  })
}
</script>

<style scoped>

.page-header{
display:flex;
justify-content:space-between;
align-items:center;
margin-bottom:30px;
}

.btn-primary{
background:#3B82F6;
color:white;
padding:12px 20px;
border:none;
border-radius:8px;
cursor:pointer;
}

</style>
