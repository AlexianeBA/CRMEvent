import { defineStore } from "pinia"
import invoiceService from "@/services/invoiceService"

export const useInvoiceStore = defineStore("invoice", {
  state: () => ({
    invoices: [],
    loading: false,
  }),

  actions: {
    async loadInvoices() {
      this.loading = true
      try {
        this.invoices = await invoiceService.getInvoices()
      } finally {
        this.loading = false
      }
    },

    async deleteInvoice(id) {
      await invoiceService.delete(id)
      await this.loadInvoices()
    },
  },
})
