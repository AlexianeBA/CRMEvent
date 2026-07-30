<template>

<div class="card">

<div class="toolbar">

<input
v-model="search"
placeholder="Rechercher..."
class="search"
/>

</div>

<table>

<thead>

<tr>
<th>Nom</th>
<th>Adresse</th>
<th>Ville</th>
</tr>

</thead>

<tbody>

<tr
v-for="company in filteredCompanies"
:key="company.id"
>

<td>{{ company.name }}</td>
<td>{{ company.address }}</td>
<td>{{ company.city }}</td>


</tr>

</tbody>

</table>

</div>

</template>

<script setup>
import { computed, ref, onMounted } from "vue"
import { useCompanyStore } from "@/stores/company"

const store = useCompanyStore()

const search = ref("")

onMounted(() => {
    store.loadCompanies()
})

const filteredCompanies = computed(() => {

    return store.companies.filter(company =>

        company.name.toLowerCase().includes(search.value.toLowerCase())

    )

})

</script>

<style scoped>

.card{
background:white;
border-radius:12px;
padding:25px;
}

.toolbar{
margin-bottom:20px;
}

.search{
width:350px;
padding:10px;
}

table{
width:100%;
border-collapse:collapse;
}

th,
td{
padding:15px;
text-align:left;
border-bottom:1px solid #eee;
}

</style>