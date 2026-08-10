<template>
  <DashboardLayout>

    <div class="page-header">
      <div>
        <h1>Contacts</h1>
        <p>Gestion des contacts clients</p>
      </div>

      <v-btn
        color="primary"
        prepend-icon="mdi-plus"
        @click="goToCreate"
      >
        Nouveau contact
      </v-btn>
    </div>

    <ContactTable />

  </DashboardLayout>
</template>

<script setup>
import { useRouter } from "vue-router"
import DashboardLayout from "@/layouts/DashboardLayout.vue"
import ContactTable from "@/components/contact/ContactTable.vue"

const router = useRouter()

function goToCreate() {
  router.push({
    name: "ContactCreate",
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