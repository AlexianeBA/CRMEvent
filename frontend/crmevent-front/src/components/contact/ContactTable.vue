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
<th>Prénom</th>
<th>Téléphone</th>
<th>Email</th>
</tr>

</thead>

<tbody>

<tr
v-for="contact in filteredContacts"
:key="contact.id"
>

<td>{{ contact.first_name }}</td>
<td>{{ contact.last_name }}</td>
<td>{{ contact.phone_number }}</td>
<td>{{ contact.email }}</td>

</tr>

</tbody>

</table>

</div>

</template>

<script setup>
import { computed, ref, onMounted } from "vue"
import { useContactStore } from "@/stores/contact"

const store = useContactStore()

const search = ref("")

onMounted(() => {
    store.loadContacts()
})

const filteredContacts = computed(() => {
  return store.contacts.filter(contact => {
    const fullname = `${contact.first_name} ${contact.last_name}`.toLowerCase()
    return fullname.includes(search.value.toLowerCase())
  })
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