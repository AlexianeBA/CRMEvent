import { defineStore } from "pinia";
import eventService  from "@/services/eventService";

export const useEventStore = defineStore("event", {
  state: () => ({
    events: [],
    loading: false,
  }),

  getters: {
    nextEvent(state) {
      if (state.events.length === 0) return null;

      return state.events[0];
    },
  },

  actions: {
      async loadEvents() {
        this.loading = true

        try {
          this.events =
            await eventService.getEvents()
        } finally {
          this.loading = false
        }
      },

      async deleteEvent(id) {
        await eventService.delete(id)
        await this.loadEvents()
      },
    },
  },
)