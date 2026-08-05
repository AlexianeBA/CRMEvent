<template>
  <div class="details-card">
    <div class="card-title">
      <v-icon v-if="icon" :icon="icon" />

      <h2>{{ title }}</h2>
    </div>

    <div class="details-list">
      <div
        v-for="field in fields"
        :key="field.key"
        class="detail-item"
      >
        <span>{{ field.label }}</span>

        <slot
          :name="`field-${field.key}`"
          :value="getValue(field)"
          :item="item"
        >
          <strong>
            {{ formatValue(field) }}
          </strong>
        </slot>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  title: {
    type: String,
    required: true,
  },
  icon: {
    type: String,
    default: "",
  },
  item: {
    type: Object,
    required: true,
  },
  fields: {
    type: Array,
    required: true,
  },
})

function getValue(field) {
  return field.value
    ? field.value(props.item)
    : props.item[field.key]
}

function formatValue(field) {
  const value = getValue(field)

  if (field.formatter) {
    return field.formatter(value, props.item)
  }

  return value ?? "—"
}
</script>

<style scoped>
.details-card {
  padding: 24px;
  background: white;
  border-radius: 14px;
}

.card-title {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 22px;
}

.card-title h2 {
  margin: 0;
  font-size: 18px;
}

.details-list {
  display: flex;
  flex-direction: column;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  padding: 14px 0;
  border-bottom: 1px solid #eee;
}

.detail-item:last-child {
  border-bottom: 0;
}

.detail-item span {
  color: #777;
}

.detail-item strong {
  text-align: right;
}
</style>