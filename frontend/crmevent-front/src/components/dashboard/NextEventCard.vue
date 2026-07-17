<template>
  <template>

<v-card v-if="event">

  {{ event.title }}

</v-card>

<v-card v-else>

  Aucun évènement

</v-card>

</template>
</template>

<script setup>
import { computed, onMounted } from "vue";
import { useEventStore } from "@/stores/event";

const store = useEventStore();

onMounted(() => {
  store.loadEvents();
});

const event = computed(() => store.nextEvent);
</script>

<style scoped>

.next-event{

background:linear-gradient(180deg,#5B5CEB,#6868FF);

color:white;

padding:25px;

overflow:hidden;

position:relative;

}

.next-event::after{

content:"";

position:absolute;

width:260px;

height:260px;

border-radius:50%;

background:rgba(255,255,255,.08);

bottom:-120px;

right:-80px;

}

.top{

display:flex;

justify-content:space-between;

align-items:center;

margin-bottom:25px;

}

.label{

font-weight:600;

font-size:15px;

}

.title{

font-size:24px;

font-weight:700;

margin-bottom:5px;

}

.location{

opacity:.8;

margin-bottom:20px;

}

.infos{

display:flex;

justify-content:space-between;

margin-bottom:25px;

}

.infos div{

display:flex;

flex-direction:column;

}

.infos span{

font-size:12px;

opacity:.7;

}

.price{

margin-top:15px;

display:flex;

flex-direction:column;

}

.price span{

font-size:12px;

opacity:.7;

}

.price strong{

font-size:24px;

margin-top:5px;

}

</style>