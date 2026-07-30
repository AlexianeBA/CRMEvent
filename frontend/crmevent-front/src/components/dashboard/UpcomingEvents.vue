<template>
  <v-card class="next-card" rounded="xl" elevation="0">

    <div v-if="store.loading">
      Chargement...
    </div>

    <template v-else-if="event">

      <span class="badge">
        Prochain événement
      </span>

      <h2>{{ event.title }}</h2>

      <p>{{ event.location }}</p>

      <div class="infos">
        <div>
          <small>Date</small>
          <strong>{{ event.date }}</strong>
        </div>

        <div>
          <small>Durée</small>
          <strong>{{ event.duration }} h</strong>
        </div>
      </div>

      <v-btn
        color="white"
        rounded
        block
      >
        Voir l'événement
      </v-btn>

    </template>

    <div v-else>
      Aucun événement
    </div>

  </v-card>
</template>

<script setup>
import { computed, onMounted } from "vue";
import { useEventStore } from "@/stores/event";

const store = useEventStore();

onMounted(() => {
  if (!store.events.length)
    store.loadEvents();
});

const event = computed(() => {
  return store.events.length ? store.events[0] : null;
});
</script>

<style scoped>
.next-card{
    background:#5b5ce6;
    color:white;
    padding:24px;
}

.badge{
    display:inline-block;
    background:rgba(255,255,255,.2);
    padding:6px 12px;
    border-radius:20px;
    margin-bottom:20px;
}

.infos{
    display:flex;
    justify-content:space-between;
    margin:30px 0;
}
</style>