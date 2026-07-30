<template>
  <DashboardLayout>

    <div class="page-header">
      <div>
        <h1>Contacts</h1>
        <p>Gestion des contacts clients</p>
      </div>

      <button class="btn-primary">
        Nouveau contact
      </button>
    </div>

    <ContactTable />

  </DashboardLayout>
</template>

<script setup>
import DashboardLayout from "@/layouts/DashboardLayout.vue"
import ContactTable from "@/components/contact/ContactTable.vue"
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