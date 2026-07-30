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
<th>Titre</th>
<th>Type</th>
<th>Date</th>
<th>Durée</th>
<th>Localisation</th>
</tr>

</thead>

<tbody>

<tr
v-for="event in filteredEvents"
:key="event.id"
>

<td>{{ event.title }}</td>
<td>{{ event.type }}</td>
<td>{{ event.date }}</td>
<td>{{ event.duration }}</td>
<td>{{ event.location }}</td>

</tr>

</tbody>

</table>

</div>

</template>

<script setup>
import { computed, ref, onMounted } from "vue"
import { useEventStore } from "@/stores/event"

const store = useEventStore()

const search = ref("")

onMounted(() => {
    store.loadEvents()
})

const filteredEvents = computed(() => {
  return store.events.filter(event => {
    const title = event.title.toLowerCase()
    return title.includes(search.value.toLowerCase())
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