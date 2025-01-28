<template>
  <div>
    <h1>Utilisateurs:</h1>
    <ul>
      <li v-for="user in users" :key="user[0]">
        <strong>Name:</strong> {{ user[1] }}<br />
        <strong>Email:</strong> {{ user[2] }}<br />
        <strong>Username:</strong> {{ user[3] }}
        <hr />
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import apiClient from '~/services/api.js';

const users = ref([]);

onMounted(async () => {
  try {
    const response = await apiClient.get('/users'); 
    users.value = response.data.data;
  } catch (error) {
    console.error('Error fetching API:', error);
  }
});
</script>
