<template>
  <div class="stats-grid">
    <template v-if="loading">
      <v-skeleton-loader v-for="index in 6" :key="index" type="article" />
    </template>
    <template v-else>
      <button v-for="stat in stats" :key="stat.label" class="stat-card" type="button" @click="router.push({ name: stat.route })">
        <v-avatar :color="stat.color" variant="tonal" size="46"><v-icon :icon="stat.icon" /></v-avatar>
        <div><span>{{ stat.label }}</span><strong>{{ stat.value }}</strong></div>
      </button>
    </template>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router"
defineProps({ loading: Boolean, stats: { type: Array, default: () => [] } })
const router = useRouter()
</script>

<style scoped>
.stats-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px; }
.stat-card { display: flex; align-items: center; gap: 14px; padding: 18px; border: 0; border-radius: 14px; background: white; text-align: left; cursor: pointer; box-shadow: 0 1px 3px rgb(15 23 42 / 8%); }
.stat-card:hover { transform: translateY(-1px); box-shadow: 0 8px 22px rgb(15 23 42 / 10%); }
.stat-card span, .stat-card strong { display: block; }
.stat-card span { color: #64748b; font-size: 13px; }
.stat-card strong { margin-top: 2px; color: #0f172a; font-size: 25px; }
@media (max-width: 850px) { .stats-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 520px) { .stats-grid { grid-template-columns: 1fr; } }
</style>
