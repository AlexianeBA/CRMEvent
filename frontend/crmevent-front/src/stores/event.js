import { defineStore } from "pinia";
import { getEvents } from "@/services/eventService";

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
      this.loading = true;

      try {
        const response = await getEvents();
        this.events = response.data;
      } finally {
        this.loading = false;
      }
    },
  },
});