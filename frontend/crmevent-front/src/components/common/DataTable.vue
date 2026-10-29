<template>
  <div class="card">
    <ListControls :list="list" />

    <div v-if="list.loading" class="state-message">Chargement...</div>

    <div v-else-if="list.items.length === 0" class="state-message">Aucun résultat</div>

    <div v-else class="table-scroll">
      <table>
        <thead>
          <tr>
            <th v-for="column in columns" :key="column.key" :aria-sort="ariaSort(column.key)">
              <button
                v-if="list.meta.sortable.includes(column.key)"
                class="sort-button"
                @click="list.sort(column.key)"
              >
                {{ column.label }}
                <span v-if="list.params.sort_by === column.key">{{
                  list.params.sort_order === 'asc' ? '↑' : '↓'
                }}</span>
              </button>
              <span v-else>{{ column.label }}</span>
            </th>

            <th v-if="$slots.actions" class="actions-column">Actions</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="item in list.items" :key="item[itemKey]">
            <td v-for="column in columns" :key="column.key">
              <slot :name="`cell-${column.key}`" :item="item" :value="item[column.key]">
                {{ formatValue(item, column) }}
              </slot>
            </td>

            <td v-if="$slots.actions" class="actions-cell">
              <slot name="actions" :item="item" />
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <ListPagination :list="list" />
  </div>
</template>

<script setup>
import { useListing } from '@/composables/useListing'
import ListControls from '@/components/common/ListControls.vue'
import ListPagination from '@/components/common/ListPagination.vue'

const props = defineProps({
  resource: { type: String, required: true },
  columns: { type: Array, required: true },
  itemKey: { type: String, default: 'id' },
  scope: { type: Object, default: () => ({}) },
  queryPrefix: { type: String, default: '' },
})
const list = useListing(() => props.resource, {
  scope: () => props.scope,
  prefix: () => props.queryPrefix,
})
defineExpose({ reload: list.reload })

function ariaSort(key) {
  if (list.params.sort_by !== key) return 'none'
  return list.params.sort_order === 'asc' ? 'ascending' : 'descending'
}

function formatValue(item, column) {
  const value = item[column.key]
  return column.formatter ? column.formatter(value, item) : (value ?? '—')
}
</script>

<style scoped>
.card {
  background: white;
  border-radius: 12px;
  padding: 25px;
}

.table-scroll {
  overflow-x: auto;
}
.sort-button {
  cursor: pointer;
  font: inherit;
  color: inherit;
  text-align: left;
  width: 100%;
}
.sort-button:focus-visible {
  outline: 2px solid #2563eb;
  outline-offset: 4px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  padding: 15px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

th {
  font-weight: 600;
}

.state-message {
  padding: 30px;
  text-align: center;
  color: #777;
}
.actions-column,
.actions-cell {
  width: 140px;
  text-align: right;
  white-space: nowrap;
}
</style>
