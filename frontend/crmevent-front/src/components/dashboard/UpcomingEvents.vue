<template>
  <v-card class="next-card" rounded="xl" elevation="0">
    <v-skeleton-loader v-if="loading" type="article" />
    <template v-else-if="nextEvent">
      <span class="badge">Prochain événement</span>
      <h2>{{ nextEvent.title }}</h2>
      <p><v-icon icon="mdi-map-marker-outline" size="18" /> {{ nextEvent.location }}</p>
      <div class="infos">
        <div><small>Date</small><strong>{{ formatDate(nextEvent.date) }}</strong></div>
        <div><small>Durée</small><strong>{{ nextEvent.duration }} h</strong></div>
        <div><small>Statut</small><strong>{{ nextEvent.status }}</strong></div>
      </div>
      <v-btn color="white" variant="flat" rounded block @click="router.push({ name: 'EventView', params: { id: nextEvent.id } })">Voir l'événement</v-btn>
    </template>
    <div v-else class="empty">Aucun événement planifié</div>
  </v-card>
</template>

<script setup>
import { computed } from "vue"
import { useRouter } from "vue-router"
const props = defineProps({ loading: Boolean, events: { type: Array, default: () => [] } })
const router = useRouter()

function parseDate(value) {
  if (!value) return null
  const parts = value.split("-")
  if (parts[0]?.length === 2) return new Date(`${parts[2]}-${parts[1]}-${parts[0]}T00:00:00`)
  return new Date(`${value}T00:00:00`)
}

const nextEvent = computed(() => props.events
  .filter((event) => !["held", "canceled", "locked"].includes(event.status))
  .map((event) => ({ event, date: parseDate(event.date) }))
  .filter(({ date }) => {
    if (!date || Number.isNaN(date.getTime())) return false
    const today = new Date()
    today.setHours(0, 0, 0, 0)
    return date >= today
  })
  .sort((a, b) => a.date - b.date)[0]?.event ?? null)

function formatDate(value) {
  const date = parseDate(value)
  return date ? new Intl.DateTimeFormat("fr-FR", { dateStyle: "long" }).format(date) : value
}
</script>

<style scoped>
.next-card { background: linear-gradient(135deg, #5b5ce6, #7c3aed); color: white; padding: 26px; min-height: 250px; }
.badge { display: inline-block; background: rgb(255 255 255 / 18%); padding: 6px 12px; border-radius: 20px; margin-bottom: 18px; }
h2 { margin: 0 0 8px; }.next-card p { display: flex; align-items: center; gap: 5px; opacity: .9; }
.infos { display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; margin: 28px 0; }
.infos small, .infos strong { display: block; }.infos small { opacity: .7; }.infos strong { margin-top: 4px; }
.empty { display: grid; place-items: center; min-height: 190px; }
</style>
