<template>
  <v-card class="history-card">
    <div class="history-header">
      <div>
        <h3>Historique</h3>
        <p>Dernières actions liées à cette fiche</p>
      </div>
      <v-btn icon="mdi-refresh" variant="text" :loading="loading" title="Rafraîchir" @click="loadHistory" />
    </div>

    <v-alert v-if="error" type="error" variant="tonal" class="ma-5">{{ error }}</v-alert>
    <div v-else-if="loading && entries.length === 0" class="history-state">Chargement...</div>
    <div v-else-if="entries.length === 0" class="history-state">Aucune action enregistrée pour le moment</div>
    <v-timeline v-else side="end" density="compact" align="start" class="history-timeline">
      <v-timeline-item
        v-for="entry in entries"
        :key="entry.id"
        :dot-color="actionColors[entry.action] ?? 'primary'"
        :icon="actionIcons[entry.action] ?? 'mdi-history'"
        size="small"
      >
        <div class="entry">
          <div class="entry-heading">
            <strong>{{ entry.message }}</strong>
            <time>{{ formatDate(entry.created_at) }}</time>
          </div>
          <div class="entry-meta">
            <v-chip size="x-small" variant="tonal">{{ entityLabels[entry.entity_type] ?? entry.entity_type }}</v-chip>
            <span>{{ entry.user_email }}</span>
          </div>
        </div>
      </v-timeline-item>
    </v-timeline>
  </v-card>
</template>

<script setup>
import { onMounted, ref, watch } from "vue"
import historyService from "@/services/historyService"

const props = defineProps({
  entityType: { type: String, required: true },
  entityId: { type: [Number, String], required: true },
})

const entries = ref([])
const loading = ref(false)
const error = ref("")
const actionColors = { created: "success", updated: "blue", status_changed: "orange", deleted: "error" }
const actionIcons = { created: "mdi-plus", updated: "mdi-pencil", status_changed: "mdi-swap-horizontal", deleted: "mdi-delete" }
const entityLabels = { company: "Entreprise", contact: "Contact", opportunity: "Opportunité", event: "Événement", quote: "Devis", invoice: "Facture" }

async function loadHistory() {
  if (!props.entityId) return
  loading.value = true
  error.value = ""
  try {
    entries.value = await historyService.getHistory({
      [`${props.entityType}_id`]: Number(props.entityId),
      limit: 100,
    })
  } catch (err) {
    error.value = err.response?.data?.detail ?? "Impossible de charger l'historique"
  } finally {
    loading.value = false
  }
}

function formatDate(value) {
  if (!value) return "—"
  return new Intl.DateTimeFormat("fr-FR", { dateStyle: "medium", timeStyle: "short" }).format(new Date(value))
}

watch(() => [props.entityType, props.entityId], loadHistory)
onMounted(loadHistory)
</script>

<style scoped>
.history-card { margin-top: 24px; padding-bottom: 8px; }
.history-header { display: flex; align-items: center; justify-content: space-between; padding: 20px 24px; border-bottom: 1px solid #eee; }
.history-header h3, .history-header p { margin: 0; }
.history-header p { margin-top: 4px; color: #6b7280; }
.history-state { padding: 36px; text-align: center; color: #6b7280; }
.history-timeline { padding: 20px 24px; }
.entry { min-width: 0; padding-bottom: 8px; }
.entry-heading { display: flex; justify-content: space-between; gap: 20px; }
.entry-heading time { color: #6b7280; white-space: nowrap; font-size: 0.85rem; }
.entry-meta { display: flex; align-items: center; gap: 10px; margin-top: 7px; color: #6b7280; font-size: 0.85rem; }
@media (max-width: 700px) { .entry-heading { flex-direction: column; gap: 4px; } }
</style>
