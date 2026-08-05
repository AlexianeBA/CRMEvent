<template>
  <DashboardLayout>
    <div class="page-header">
      <div>
        <h1>Entreprises</h1>

        <p>
          Gestion des entreprises clientes
        </p>
      </div>

      <v-btn
        color="primary"
        prepend-icon="mdi-plus"
        @click="goToCreate"
      >
        Nouvelle entreprise
      </v-btn>
    </div>

    <CompanyTable />
  </DashboardLayout>
</template>

<script setup>
import { useRouter } from "vue-router"

import DashboardLayout from "@/layouts/DashboardLayout.vue"
import CompanyTable from "@/components/company/CompanyTable.vue"

const router = useRouter()

function goToCreate() {
  router.push({
    name: "CompanyCreate",
  })
}
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 24px;
  margin-bottom: 30px;
}

.page-header h1 {
  margin: 0;
  color: #1f2937;
  font-size: 30px;
  font-weight: 700;
}

.page-header p {
  margin: 6px 0 0;
  color: #6b7280;
}

@media (max-width: 700px) {
  .page-header {
    align-items: flex-start;
    flex-direction: column;
  }
}
</style>