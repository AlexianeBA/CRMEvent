<template>

<div class="card">

<div class="toolbar">
<v-text-field v-model="search" label="Rechercher" variant="solo" class="w-100"></v-text-field>


</div>

<table>

<thead>

<tr>
<th>Numéro</th>
<th>Titre</th>
<th>Total</th>
<th>Statut</th>
</tr>

</thead>

<tbody>

<tr
v-for="quote in filteredQuotes"
:key="quote.id"
>

<td>{{ quote.number }}</td>
<td>{{ quote.title }}</td>
<td>{{ quote.total_amount }}</td>
<td>{{ quote.status }}</td>


</tr>

</tbody>

</table>

</div>

</template>

<script setup>
import { computed, ref, onMounted } from "vue"
import { useQuoteStore } from "@/stores/quotes"

const store = useQuoteStore()

const search = ref("")

onMounted(() => {
    store.loadQuotes()
})

const filteredQuotes = computed(() => {
  return store.quotes.filter(quote => {
    const title = quote.title.toLowerCase()
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