<template>
  <section class="page">
    <div class="page-header">
      <div>
        <p v-if="breadcrumb" class="breadcrumb">
          {{ breadcrumb }}
        </p>

        <h1>{{ title }}</h1>

        <p v-if="subtitle" class="subtitle">
          {{ subtitle }}
        </p>
      </div>

      <div class="header-actions">
        <v-btn
          variant="outlined"
          prepend-icon="mdi-arrow-left"
          @click="$emit('back')"
        >
          Retour
        </v-btn>

        <v-btn
          v-if="showEdit"
          color="primary"
          prepend-icon="mdi-pencil-outline"
          @click="$emit('edit')"
        >
          Modifier
        </v-btn>

        <slot name="actions" />
      </div>
    </div>

    <v-progress-linear
      v-if="loading"
      indeterminate
      color="primary"
    />

    <v-alert
      v-else-if="error"
      type="error"
      variant="tonal"
    >
      {{ error }}
    </v-alert>

    <div v-else>
      <slot />
    </div>
  </section>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true,
  },
  subtitle: {
    type: String,
    default: "",
  },
  breadcrumb: {
    type: String,
    default: "",
  },
  loading: {
    type: Boolean,
    default: false,
  },
  error: {
    type: String,
    default: "",
  },
  showEdit: {
    type: Boolean,
    default: true,
  },
})

defineEmits(["back", "edit"])
</script>

<style scoped>
.page {
  padding: 30px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 24px;
  margin-bottom: 28px;
}

.breadcrumb {
  margin: 0 0 4px;
  color: #8b644b;
  font-size: 13px;
}

.subtitle {
  margin: 6px 0 0;
  color: #777;
}

h1 {
  margin: 0;
  font-size: 28px;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

@media (max-width: 700px) {
  .page-header {
    flex-direction: column;
  }
}
</style>