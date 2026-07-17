<template>

<div class="sidebar">

    <h2>CRM</h2>

    <RouterLink to="/dashboard">Tableau de bord</RouterLink>

    <RouterLink to="/companies">Entreprises</RouterLink>

    <RouterLink to="/contacts">Contacts</RouterLink>

    <RouterLink to="/opportunities">Pipeline</RouterLink>

    <RouterLink to="/events">Evènements</RouterLink>

    <RouterLink to="/quotes">Devis</RouterLink>

    <RouterLink to="/invoices">Factures</RouterLink>

</div>

</template>

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

</style>