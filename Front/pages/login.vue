<template>
  <div class="upload-form">
    <h1>S'authentifier</h1>
    <form @submit.prevent="login">
      <div class="form-group">
        <label for="username">Pseudo:</label>
        <br />
        <br />
        <input
          type="text"
          id="username"
          v-model="username"
          class="form-control"
        />
      </div>
      <br />
      <br />
      <div class="form-group">
        <label for="password">Mot de passe:</label>
        <br />
        <br />
        <input
          type="password"
          id="password"
          v-model="password"
          class="form-control"
        />
      </div>
      <br />
      <br />
      <button type="submit" class="btn btn-primary">S'authentifier</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import apiClient from "~/services/api.js";
import { useRouter } from "vue-router";
import jwt_decode from "jwt-decode";
import nuxtStorage from "nuxt-storage";

const username = ref("");
const password = ref("");
const router = useRouter();

async function login() {
  try {
    const response = await apiClient.post("/auth", {
      username: username.value,
      password: password.value,
    });

    if (response.data && response.data.data.token) {
      // Sauvegarde le token dans le local storage
      const token = response.data.data.token;
      nuxtStorage.localStorage.setData("token", token, 2, "h");

      // Décode le token pour récupérer l'id de l'utilisateur
      const decodedToken = jwt_decode(token);

      // Ajoute le token dans les headers de toutes les requêtes
      // apiClient.defaults.headers.common["Authorization"] = `Bearer ${token}`;

      router.push("/dashboard");
    } else {
      router.push("/");
    }
  } catch (error) {
    console.error("Error during login:", error);
  }
}
</script>

<style scoped>
.upload-form {
  max-width: 700px;
  margin: auto;
  margin-top: 50px;
  padding: 20px;
  background-color: #0f0f0f;
}

.form-group {
  margin-bottom: 20px;
}

label {
  font-weight: bold;
  color: #ffffff;
}

.form-control {
  width: 100%;
  padding: 10px;
  border-top: none;
  border-right: none;
  border-left: none;
  border-bottom: bottom 1px #ffffff;
  font-size: 16px;
  background-color: #0f0f0f;
  color: #ffffff;
  border-radius: 0px;
}

.form-control:focus {
  outline: none !important; 
}

.form-control-file {
  width: 100%;
  padding: 10px;
}

.btn-primary {
  background-color: rgb(14, 211, 27);
  color: #fff;
  padding: 10px 20px;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}

.btn-primary:hover {
  background-color: rgb(10, 83, 15);
}

h1 {
  color: #fff;
  padding: 30px;
}
</style>
