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
import api from "../api/api";
import { useRouter } from "vue-router";

const router = useRouter();

const email = ref("");
const password = ref("");

const login = async () => {
  try {
    const formData = new URLSearchParams();
    formData.append("username", email.value);
    formData.append("password", password.value);

    const res = await api.post("/auth/login", formData);

    localStorage.setItem("token", res.data.access_token);

    router.push("/dashboard");
  } catch (err) {
    alert("Identifiants invalides");
  }
};
</script>