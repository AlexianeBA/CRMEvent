<template>

<div class="sidebar">

    <h2>CRM</h2>

    <RouterLink to="/dashboard">Tableau de bord</RouterLink>

    <RouterLink to="/companies">Entreprises</RouterLink>

    <RouterLink to="/contacts">Contacts</RouterLink>

    <RouterLink to="/opportunities">Opportunités</RouterLink>

    <RouterLink to="/events">Evènements</RouterLink>

    <RouterLink to="/quotes">Devis</RouterLink>

    <RouterLink to="/invoices">Factures</RouterLink>

    <RouterLink v-if="auth.isAdmin" to="/admin/users">Administration</RouterLink>

    <div class="account">
      <span>{{ auth.user?.email }}</span>
      <small>{{ roleLabels[auth.user?.role] }}</small>
      <v-btn size="small" variant="tonal" prepend-icon="mdi-logout" @click="auth.logout()">
        Déconnexion
      </v-btn>
    </div>

</div>

</template>

<script setup>
import { useAuthStore } from "@/stores/auth"

defineOptions({ name: "AppSidebar" })

const auth = useAuthStore()
const roleLabels = {
  admin: "Administrateur",
  manager: "Manager",
  commercial: "Commercial",
  comptable: "Comptable",
}
</script>

<style scoped>

.sidebar{

width:240px;

background:white;

padding:30px;

display:flex;

flex-direction:column;

gap:20px;

border-right:1px solid #ececec;

}

a{

text-decoration:none;

color:#444;

}

.router-link-active{

color:#5b4df8;

font-weight:bold;

}

.account {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-top: auto;
  padding-top: 20px;
  border-top: 1px solid #ececec;
  overflow-wrap: anywhere;
}

.account small {
  color: #6b7280;
}

</style>
