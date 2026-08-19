<template>
  <DashboardLayout>

    <div class="page-header">
      <div>
        <h1>Événements</h1>
        <p>Gestion des événements</p>
      </div>

      <v-btn
        color="primary"
        prepend-icon="mdi-plus"
        @click="goToCreate"
      >
        Nouvel événement
      </v-btn>
    </div>

    <EventTable />

  </DashboardLayout>
</template>

<script setup>
import DashboardLayout from "@/layouts/DashboardLayout.vue"
import EventTable from "@/components/event/EventTable.vue"
import { useRouter } from "vue-router"

const router = useRouter()

function goToCreate() {
  router.push({
    name: "EventCreate",
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