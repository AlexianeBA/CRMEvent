import { defineStore } from "pinia"
import companyService from "@/services/contactService"

export const useContactStore = defineStore("contact", {

    state: () => ({
        contacts: [],
        loading: false
    }),

    actions: {

        async loadContacts(){

            this.loading = true

            try{
                this.contacts = await companyService.getContacts()
            }

            finally{
                this.loading = false
            }

        }

    }

})