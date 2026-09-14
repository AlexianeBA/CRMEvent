<template>
  <DashboardLayout>
    <v-container fluid>
      <div class="page-header">
        <div><h1>Notifications</h1><p>Retrouve ici tes alertes et rappels.</p></div>
        <v-btn v-if="store.unreadCount" color="primary" variant="tonal" prepend-icon="mdi-check-all" @click="store.markAllAsRead()">Tout marquer comme lu</v-btn>
      </div>

      <v-alert v-if="store.error" type="error" variant="tonal" class="mb-4">{{ store.error }}</v-alert>
      <v-card>
        <v-tabs v-model="filter">
          <v-tab value="all">Toutes</v-tab>
          <v-tab value="unread">Non lues ({{ store.unreadCount }})</v-tab>
        </v-tabs>
        <v-divider />
        <div v-if="store.loading && store.items.length === 0" class="state">Chargement...</div>
        <div v-else-if="filteredNotifications.length === 0" class="state">Aucune notification</div>
        <v-list v-else lines="three">
          <v-list-item v-for="notification in filteredNotifications" :key="notification.id" :class="{ unread: !notification.is_read }" @click="open(notification)">
            <template #prepend><v-avatar :color="severityColors[notification.severity]" variant="tonal"><v-icon :icon="typeIcons[notification.type]" /></v-avatar></template>
            <v-list-item-title>{{ notification.title }}</v-list-item-title>
            <v-list-item-subtitle>{{ notification.message }}</v-list-item-subtitle>
            <small>{{ formatDate(notification.created_at) }}</small>
            <template #append>
              <v-btn :icon="notification.is_read ? 'mdi-email-outline' : 'mdi-email-open-outline'" variant="text" :title="notification.is_read ? 'Marquer comme non lue' : 'Marquer comme lue'" @click.stop="toggleRead(notification)" />
              <v-btn icon="mdi-archive-outline" variant="text" title="Archiver" @click.stop="store.archive(notification)" />
            </template>
          </v-list-item>
        </v-list>
      </v-card>
    </v-container>
  </DashboardLayout>
</template>

<script setup>
import { computed, onMounted, ref } from "vue"
import { useRouter } from "vue-router"
import DashboardLayout from "@/layouts/DashboardLayout.vue"
import { useNotificationStore } from "@/stores/notifications"

defineOptions({ name: "NotificationCenter" })

const router = useRouter()
const store = useNotificationStore()
const filter = ref("all")
const filteredNotifications = computed(() => filter.value === "unread" ? store.items.filter((item) => !item.is_read) : store.items)
const severityColors = { info: "primary", warning: "warning", error: "error" }
const typeIcons = { event_upcoming: "mdi-calendar-clock", opportunity_inactive: "mdi-briefcase-clock-outline", quote_unanswered: "mdi-file-clock-outline", invoice_due: "mdi-receipt-clock-outline", invoice_overdue: "mdi-alert-circle-outline", task_assigned: "mdi-clipboard-check-outline" }

async function open(notification) {
  await store.markAsRead(notification)
  if (notification.target_url) await router.push(notification.target_url)
}

function toggleRead(notification) {
  return notification.is_read ? store.markAsUnread(notification) : store.markAsRead(notification)
}

function formatDate(value) {
  return new Intl.DateTimeFormat("fr-FR", { dateStyle: "medium", timeStyle: "short" }).format(new Date(value))
}

onMounted(() => store.refresh({ synchronize: true, limit: 100 }))
</script>

<style scoped>
.page-header { display: flex; justify-content: space-between; align-items: center; gap: 20px; margin-bottom: 24px; }
.page-header h1, .page-header p { margin: 0; }
.page-header p, small { color: #6b7280; }
.state { padding: 48px; text-align: center; color: #6b7280; }
.unread { background: #eff6ff; }
@media (max-width: 700px) { .page-header { align-items: stretch; flex-direction: column; } }
</style>
