<template>
  <nav class="navbar navbar-expand-lg navbar-dark fixed-top">
    <div class="container perso_navbar">
      <a href="/"><img class="logo-nav" src="/logo_vid.png" /></a>
      <button
        class="navbar-toggler"
        type="button"
        data-toggle="collapse"
        data-target="#navbarColor02"
        aria-controls="navbarColor02"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarColor02">
        <ul class="navbar-nav mr-auto">
          <li class="nav-item" v-if="isLoggedIn">
            <router-link class="nav-link" to="/dashboard"
              >Tableau de bord</router-link
            >
          </li>
          <li class="nav-item" v-if="!isLoggedIn">
            <router-link class="nav-link" to="/login">Se connecter</router-link>
          </li>
          <li class="nav-item" v-if="!isLoggedIn">
            <router-link class="nav-link" to="/register"
              >Créer un nouveau compte</router-link
            >
          </li>
          <li class="nav-item" v-if="isLoggedIn">
            <a class="nav-link" @click="logout">Se déconnecter</a>
          </li>
          <li class="nav-item" v-if="isLoggedIn">
            <router-link class="nav-link" to="/profile">{{ username }}</router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup>
import nuxtStorage from "nuxt-storage";
import { ref } from "vue";
import { useRouter } from "vue-router";
import jwt_decode from "jwt-decode";

const isLoggedIn = ref(!!nuxtStorage.localStorage.getData("token"));
const username = ref("");

if (isLoggedIn) {
  try {
  const decodedToken = jwt_decode(nuxtStorage.localStorage.getData("token"));
  username.value = decodedToken.username;
} catch (error) {
  console.error("Error decoding JWT token:", error);
}
}

const router = useRouter();

const logout = () => {
  nuxtStorage.localStorage.removeItem("token");
  isLoggedIn.value = false;
  router.push("/login");
};

</script>

<style lang="css">
.container {
  background-color: rgb(0, 0, 0);
  padding: 5px;
}

.navbar {
  background-color: rgb(0, 0, 0);
}

.nav-item .nav-link {
  color: rgb(14, 211, 27);
  font-size: 20px;
  margin-left: 25px;
}

.navbar .navbar-brand {
  color: rgb(181, 15, 232);
}

.navbar .navbar-brand:hover {
  color: rgb(19, 210, 231);
}

.nav-item .nav-link:hover {
  color: rgb(181, 15, 232);
}

.logo-nav {
  width: 75px;
  height: 75px;
  margin-right: 50px;
}
</style>
