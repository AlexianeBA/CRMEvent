<template>
  <v-container class="fill-height d-flex align-center justify-center">
    <v-card width="400" class="pa-6">
      <h2 class="text-h5 mb-6 text-center">Connexion</h2>

      <v-form @submit.prevent="login">
        <v-text-field
          v-model="email"
          label="Email"
          type="email"
          required
        />

        <v-text-field
          v-model="password"
          label="Mot de passe"
          type="password"
          required
        />

        <v-btn
          color="primary"
          block
          class="mt-4"
          type="submit"
        >
          Se connecter
        </v-btn>
      </v-form>

      <p class="text-center mt-4">
        Pas de compte ?
        <router-link to="/register">Créer un compte</router-link>
      </p>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useRoute } from "vue-router";
import { useAuthStore } from "@/stores/auth";

defineOptions({ name: "LoginPage" });

const router = useRouter();
const route = useRoute();
const auth = useAuthStore();

const email = ref("");
const password = ref("");

const login = async () => {
  try {
    await auth.login(email.value, password.value);
    router.push(String(route.query.redirect || "/dashboard"));
  } catch (err) {
  const msg = err?.response?.data?.detail || "Erreur de connexion";
  alert(Array.isArray(msg) ? JSON.stringify(msg) : msg);
  }
};
</script>
