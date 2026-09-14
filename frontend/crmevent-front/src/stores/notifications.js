import { defineStore } from "pinia"
import notificationService from "@/services/notificationService"

export const useNotificationStore = defineStore("notifications", {
  state: () => ({
    items: [],
    unreadCount: 0,
    loading: false,
    error: "",
  }),

  actions: {
    async refresh({ synchronize = false, limit = 20 } = {}) {
      this.loading = true
      this.error = ""
      try {
        if (synchronize) await notificationService.sync()
        const [items, count] = await Promise.all([
          notificationService.list({ limit }),
          notificationService.count(),
        ])
        this.items = items
        this.unreadCount = count.unread_count
      } catch (error) {
        this.error = error.response?.data?.detail ?? "Impossible de charger les notifications"
      } finally {
        this.loading = false
      }
    },

    async markAsRead(notification) {
      if (notification.is_read) return notification
      const updated = await notificationService.markAsRead(notification.id)
      this.replace(updated)
      return updated
    },

    async markAsUnread(notification) {
      const updated = await notificationService.markAsUnread(notification.id)
      this.replace(updated)
      return updated
    },

    async markAllAsRead() {
      await notificationService.markAllAsRead()
      this.items = this.items.map((item) => ({ ...item, is_read: true }))
      this.unreadCount = 0
    },

    async archive(notification) {
      await notificationService.archive(notification.id)
      this.items = this.items.filter((item) => item.id !== notification.id)
      if (!notification.is_read) this.unreadCount = Math.max(0, this.unreadCount - 1)
    },

    replace(updated) {
      const index = this.items.findIndex((item) => item.id === updated.id)
      if (index === -1) return
      const previous = this.items[index]
      if (!previous.is_read && updated.is_read) this.unreadCount = Math.max(0, this.unreadCount - 1)
      if (previous.is_read && !updated.is_read) this.unreadCount += 1
      this.items[index] = updated
    },
  },
})
