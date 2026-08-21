import { defineStore } from "pinia"
import opportunityService from "@/services/opportunityService"

export const useOpportunityStore = defineStore("opportunity", {
  state: () => ({ opportunities: [], loading: false }),
  actions: {
    async loadOpportunities() {
      this.loading = true
      try { this.opportunities = await opportunityService.getOpportunities() }
      finally { this.loading = false }
    },
    async deleteOpportunity(id) {
      await opportunityService.delete(id)
      await this.loadOpportunities()
    },
  },
})
