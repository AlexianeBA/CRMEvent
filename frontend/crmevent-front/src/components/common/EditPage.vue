<template>
  <section class="page">
    <div class="page-header">
      <div>
        <p v-if="breadcrumb" class="breadcrumb">
          {{ breadcrumb }}
        </p>

        <h1>{{ title }}</h1>
      </div>

      <v-btn
        variant="outlined"
        prepend-icon="mdi-arrow-left"
        @click="$emit('cancel')"
      >
        Annuler
      </v-btn>
    </div>

    <v-alert
      v-if="error"
      type="error"
      variant="tonal"
      class="mb-5"
    >
      {{ error }}
    </v-alert>

    <form class="form-card" @submit.prevent="$emit('submit')">
      <slot />

      <div class="form-actions">
        <v-btn
          variant="text"
          :disabled="saving"
          @click="$emit('cancel')"
        >
          Annuler
        </v-btn>

        <v-btn
          color="primary"
          type="submit"
          :loading="saving"
          prepend-icon="mdi-content-save-outline"
        >
          Enregistrer
        </v-btn>
      </div>
    </form>
  </section>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true,
  },
  breadcrumb: {
    type: String,
    default: "",
  },
  error: {
    type: String,
    default: "",
  },
  saving: {
    type: Boolean,
    default: false,
  },
})

defineEmits(["submit", "cancel"])
</script>

<style scoped>
.page {
  padding: 30px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 28px;
}

.breadcrumb {
  margin: 0 0 4px;
  color: #8b644b;
  font-size: 13px;
}

h1 {
  margin: 0;
  font-size: 28px;
}

.form-card {
  max-width: 1000px;
  padding: 28px;
  background: white;
  border-radius: 14px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}
</style>