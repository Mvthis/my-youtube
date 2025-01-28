<template>
    <div>
      <p v-if="username">
        <UserUpdate />
    </p>
      <p v-else>Veuillez vous connecter.</p>
    </div>
  </template>
  
  <script setup>
  import nuxtStorage from "nuxt-storage";
  import jwt_decode from "jwt-decode";
  
  const token = nuxtStorage.localStorage.getData("token") || "";
  let decodedToken;
  
  try {
    decodedToken = jwt_decode(token);
  } catch (error) {
    decodedToken = null; // Provide a default value if decoding fails.
  }
  
  const username = decodedToken ? decodedToken.username : null;
  </script>

  
  