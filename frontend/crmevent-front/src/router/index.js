import { createRouter, createWebHistory } from 'vue-router'
import Home from "../pages/Home.vue"
import Login from "../pages/Login.vue"
import Register from "../pages/Register.vue"
import Dashboard from "../pages/Dashboard.vue"
import Contact from "../pages/Contacts.vue"
import Event from "../pages/Events.vue"
import Quote from "../pages/Quotes.vue"

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
    component: Contact,
  },
  {
    path: "/events",
    component: Event,
  },
  {
    path: "/quotes",
    component: Quote,
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
