import { defineStore } from "pinia"
import companyService from "@/services/companyService"

export const useCompanyStore = defineStore("company", {

    state: () => ({
        companies: [],
        loading: false
    }),

    actions: {

        async loadCompanies(){

            this.loading = true

            try{
                this.companies = await companyService.getCompanies()
            }

            finally{
                this.loading = false
            }

        },
        async deleteCompany(id) {
            await companyService.delete(id)
            await this.loadCompanies()
        }

    }

})