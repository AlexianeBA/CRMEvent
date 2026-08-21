import { createRouter, createWebHistory } from 'vue-router'
import Home from "../pages/Home.vue"
import Login from "../pages/Login.vue"
import Register from "../pages/Register.vue"
import Dashboard from "../pages/Dashboard.vue"

const routes = [
  {
    path: "/",
    component: Home,
  },
  {
    path: "/login",
    component: Login,
  },
  {
    path: "/register",
    component: Register,
  },
  {
    path: "/dashboard",
    component: Dashboard,
  },
  {
  path: "/companies",
  name: "Companies",
  component: () =>
    import("@/pages/companies/CompanyList.vue"),
  },
  {
    path: "/companies/new",
    name: "CompanyCreate",
    component: () =>
      import("@/pages/companies/CompanyCreate.vue"),
  },
  {
    path: "/companies/:id",
    name: "CompanyView",
    component: () =>
      import("@/pages/companies/CompanyView.vue"),
  },
  {
    path: "/companies/:id/edit",
    name: "CompanyEdit",
    component: () =>
      import("@/pages/companies/CompanyEdit.vue"),
  },
  {
    path: "/contacts",
    name: "Contacts",
    component: () =>
        import("@/pages/contacts/ContactList.vue"),
  },
  {
    path: "/contacts/new",
    name: "ContactCreate",
    component: () =>
      import("@/pages/contacts/ContactCreate.vue"),
  },
  {
    path: "/contacts/:id/edit",
    name: "ContactEdit",
    component: () =>
      import("@/pages/contacts/ContactEdit.vue"),
  },
   {
    path: "/contacts/:id",
    name: "ContactView",
    component: () =>
      import("@/pages/contacts/ContactView.vue"),
  },
  {
    path: "/events",
    name: "Events",
    component: () =>
      import("@/pages/events/EventList.vue"),
  },
  {
    path: "/opportunities",
    name: "Opportunities",
    component: () =>
      import("@/pages/opportunities/OpportunityList.vue"),
  },
  {
    path: "/opportunities/new",
    name: "OpportunityCreate",
    component: () =>
      import("@/pages/opportunities/OpportunityCreate.vue"),
  },
  {
    path: "/opportunities/:id/edit",
    name: "OpportunityEdit",
    component: () =>
      import("@/pages/opportunities/OpportunityEdit.vue"),
  },
  {
    path: "/opportunities/:id",
    name: "OpportunityView",
    component: () =>
      import("@/pages/opportunities/OpportunityView.vue"),
  },
  {
    path: "/events/new",
    name: "EventCreate",
    component: () =>
      import("@/pages/events/EventCreate.vue"),
  },
  {
    path: "/events/:id/edit",
    name: "EventEdit",
    component: () =>
      import("@/pages/events/EventEdit.vue"),
  },
  {
    path: "/events/:id",
    name: "EventView",
    component: () =>
      import("@/pages/events/EventView.vue"),
  },
  {
  path: "/quotes",
  name: "Quotes",
  component: () =>
    import("@/pages/quotes/QuoteList.vue"),
  },
  {
    path: "/quotes/new",
    name: "QuoteCreate",
    component: () =>
      import("@/pages/quotes/QuoteCreate.vue"),
  },
  {
    path: "/quotes/:id/edit",
    name: "QuoteEdit",
    component: () =>
      import("@/pages/quotes/QuoteEdit.vue"),
  },
  {
    path: "/quotes/:id",
    name: "QuoteView",
    component: () =>
      import("@/pages/quotes/QuoteView.vue"),
  },
  {
    path: "/invoices",
    name: "Invoices",
    component: () =>
      import("@/pages/invoices/InvoiceList.vue"),
  },
  {
    path: "/invoices/:id/edit",
    name: "InvoiceEdit",
    component: () =>
      import("@/pages/invoices/InvoiceEdit.vue"),
  },
  {
    path: "/invoices/:id",
    name: "InvoiceView",
    component: () =>
      import("@/pages/invoices/InvoiceView.vue"),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
