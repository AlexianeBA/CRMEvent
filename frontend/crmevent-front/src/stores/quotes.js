import { defineStore } from "pinia"
import companyService from "@/services/quotesService"

export const useQuoteStore = defineStore("quote", {

    state: () => ({
        quotes: [],
        loading: false
    }),

    actions: {

        async loadQuotes(){

            this.loading = true

            try{
                this.quotes = await companyService.getQuotes()
            }

            finally{
                this.loading = false
            }

        }

    }

})