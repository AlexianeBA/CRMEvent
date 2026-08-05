<template>
  <div class="card">
    <div class="toolbar">
      <v-text-field
        v-model="search"
        label="Rechercher"
        variant="solo"
        prepend-inner-icon="mdi-magnify"
        clearable
        hide-details
        class="w-100"
      />
    </div>

    <div v-if="loading" class="state-message">
      Chargement...
    </div>

    <div v-else-if="filteredItems.length === 0" class="state-message">
      Aucun résultat
    </div>

    <table v-else>
      <thead>
        <tr>
          <th
            v-for="column in columns"
            :key="column.key"
          >
            {{ column.label }}
          </th>

          <th v-if="$slots.actions" class="actions-column">
            Actions
          </th>
        </tr>
      </thead>

      <tbody>
        <tr
          v-for="item in filteredItems"
          :key="item[itemKey]"
        >
          <td
            v-for="column in columns"
            :key="column.key"
          >
            <slot
              :name="`cell-${column.key}`"
              :item="item"
              :value="item[column.key]"
            >
              {{ formatValue(item, column) }}
            </slot>
          </td>

          <td v-if="$slots.actions" class="actions-cell">
            <slot
              name="actions"
              :item="item"
            />
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { computed, ref } from "vue"

const props = defineProps({
  items: {
    type: Array,
    default: () => [],
  },
  columns: {
    type: Array,
    required: true,
  },
  searchFields: {
    type: Array,
    default: () => [],
  },
  itemKey: {
    type: String,
    default: "id",
  },
  loading: {
    type: Boolean,
    default: false,
  },
})

const search = ref("")

const filteredItems = computed(() => {
  const normalizedSearch = search.value.trim().toLowerCase()

  if (!normalizedSearch) {
    return props.items
  }

  return props.items.filter((item) =>
    props.searchFields.some((field) => {
      const value = item[field]

      return String(value ?? "")
        .toLowerCase()
        .includes(normalizedSearch)
    }),
  )
})

function formatValue(item, column) {
  const value = item[column.key]

  if (column.formatter) {
    return column.formatter(value, item)
  }

  return value ?? "—"
}
</script>

<style scoped>
.card {
  background: white;
  border-radius: 12px;
  padding: 25px;
}

.toolbar {
  margin-bottom: 20px;
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