import { defineStore } from "pinia"
import quoteService from "@/services/quotesService"

export const useQuoteStore = defineStore("quote", {

    state: () => ({
        quotes: [],
        loading: false
    }),

    actions: {

        async loadQuotes(){

            this.loading = true

            try{
                this.quotes = await quoteService.getQuotes()
            }

            finally{
                this.loading = false
            }

        },

        async deleteQuote(id) {
            await quoteService.delete(id)
            await this.loadQuotes()
        }

    }

})
