<template>
  <div class="list-filters">
    <v-text-field
      v-model="search"
      label="Rechercher"
      prepend-inner-icon="mdi-magnify"
      variant="outlined"
      density="compact"
      hide-details
      clearable
    />
    <v-select
      v-if="list.meta.statuses.length"
      :model-value="list.params.status ?? null"
      :items="list.meta.statuses"
      :label="list.meta.status_label"
      clearable
      variant="outlined"
      density="compact"
      hide-details
      @update:model-value="list.update({ status: $event })"
    />
    <v-autocomplete
      v-if="list.meta.company && !list.fixedFilters.includes('company_id')"
      :model-value="Number(list.params.company_id) || null"
      :items="list.options.companies"
      label="Entreprise"
      clearable
      variant="outlined"
      density="compact"
      hide-details
      @update:model-value="list.update({ company_id: $event })"
    />
    <v-autocomplete
      v-if="list.meta.commercial"
      :model-value="Number(list.params.commercial_id) || null"
      :items="list.options.commercials"
      label="Commercial / responsable"
      clearable
      variant="outlined"
      density="compact"
      hide-details
      @update:model-value="list.update({ commercial_id: $event })"
    />
    <template v-if="list.meta.period_label">
      <v-text-field
        :model-value="list.params.date_from || ''"
        type="date"
        :label="`${list.meta.period_label} : du`"
        variant="outlined"
        density="compact"
        hide-details
        clearable
        @update:model-value="list.update({ date_from: $event })"
      />
      <v-text-field
        :model-value="list.params.date_to || ''"
        type="date"
        label="Au (inclus)"
        variant="outlined"
        density="compact"
        hide-details
        clearable
        @update:model-value="list.update({ date_to: $event })"
      />
    </template>
  </div>
  <div class="list-actions">
    <template v-if="showSort">
      <v-select
        :model-value="list.params.sort_by"
        :items="list.meta.sort_options || []"
        label="Trier par"
        variant="outlined"
        density="compact"
        hide-details
        class="sort-field"
        @update:model-value="list.update({ sort_by: $event })"
      />
      <v-btn
        variant="text"
        size="small"
        @click="list.update({ sort_order: list.params.sort_order === 'asc' ? 'desc' : 'asc' })"
      >
        {{ list.params.sort_order === 'asc' ? 'Croissant ↑' : 'Décroissant ↓' }}
      </v-btn>
    </template>
    <v-btn variant="text" size="small" @click="reset">Réinitialiser</v-btn>
    <v-btn variant="text" size="small" :loading="list.loading" @click="list.reload"
      >Actualiser</v-btn
    >
    <v-spacer />
    <v-btn variant="tonal" size="small" :disabled="list.exporting" @click="list.exportFile('csv')"
      >CSV</v-btn
    >
    <v-btn variant="tonal" size="small" :loading="list.exporting" @click="list.exportFile('xlsx')"
      >Excel</v-btn
    >
  </div>
  <v-alert v-if="list.error" type="error" variant="tonal" class="mb-4" role="alert">{{
    list.error
  }}</v-alert>
</template>

<script setup>
import { onScopeDispose, ref, watch } from 'vue'
const props = defineProps({
  list: { type: Object, required: true },
  showSort: { type: Boolean, default: false },
})
const search = ref(props.list.params.q || '')
let timer
watch(
  () => props.list.params.q,
  (value) => {
    clearTimeout(timer)
    search.value = value || ''
  },
)
watch(search, (value) => {
  clearTimeout(timer)
  if ((value || '') === (props.list.params.q || '')) return
  timer = setTimeout(() => props.list.update({ q: value }), 300)
})
onScopeDispose(() => clearTimeout(timer))
function reset() {
  search.value = ''
  clearTimeout(timer)
  return props.list.reset()
}
</script>

<style scoped>
.list-filters {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
  gap: 12px;
  margin-bottom: 14px;
}
.list-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
  margin-bottom: 14px;
}
.sort-field {
  flex: 0 1 200px;
  min-width: 150px;
}
</style>
