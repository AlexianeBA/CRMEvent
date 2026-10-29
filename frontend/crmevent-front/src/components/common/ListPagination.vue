<template>
  <nav class="list-pagination" aria-label="Pagination">
    <span role="status">{{ list.total }} résultat(s)</span>
    <v-select
      :model-value="list.params.page_size"
      :items="[10, 20, 50, 100]"
      label="Par page"
      variant="outlined"
      density="compact"
      hide-details
      class="page-size"
      @update:model-value="list.update({ page_size: $event })"
    />
    <v-btn
      variant="text"
      size="small"
      :disabled="list.loading || list.params.page <= 1"
      @click="list.update({ page: list.params.page - 1 }, false)"
      >Précédent</v-btn
    >
    <span>Page {{ list.params.page }} / {{ Math.max(1, list.pages) }}</span>
    <v-btn
      variant="text"
      size="small"
      :disabled="list.loading || list.params.page >= list.pages"
      @click="list.update({ page: list.params.page + 1 }, false)"
      >Suivant</v-btn
    >
  </nav>
</template>

<script setup>
defineProps({ list: { type: Object, required: true } })
</script>

<style scoped>
.list-pagination {
  display: flex;
  justify-content: flex-end;
  flex-wrap: wrap;
  align-items: center;
  gap: 12px;
  padding-top: 20px;
}
.page-size {
  flex: 0 0 110px;
}
</style>
