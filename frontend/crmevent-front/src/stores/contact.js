import { defineStore } from "pinia"
import contactService from "@/services/contactService"

export const useContactStore = defineStore("contact", {

    state: () => ({
        contacts: [],
        loading: false
    }),

    actions: {

        async loadContacts(){

            this.loading = true

            try{
                this.contacts = await contactService.getContacts()
            }

            finally{
                this.loading = false
            }

        },
        async deleteContact(id) {
            await contactService.delete(id)
            await this.loadContacts()
        }

    }

})