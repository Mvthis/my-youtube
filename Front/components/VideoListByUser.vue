<template>
  <div class="video-card-list">
    <div v-for="video in videos" :key="video.id">
      <VideoCard
        :video="{
          id: video.id,
          name: video.name,
          image: video.image,
          description: video.description,
          duration: video.duration + ' secondes',
          creator: video.username,
          views: 10,
        }"
      />
      <hr />
    </div>
  </div>
</template>

<script setup>
import nuxtStorage from "nuxt-storage";
import { ref, onMounted } from "vue";
import apiClient from "~/services/api.js";
import jwt_decode from "jwt-decode";

const videos = ref([]);

onMounted(async () => {
  try {
    const token = nuxtStorage.localStorage.getData("token") || "";
    if (!token) {
      console.error("Token not found");
    }
    const decodedToken = jwt_decode(token);
    const user_id = decodedToken.id;
    const response = await apiClient.get("/user/" + user_id + "/videos");
    videos.value = response.data.data;
  } catch (error) {
    console.error("Error fetching API:", error);
  }
});
</script>

<style scoped>
.video-card-list {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
}

hr {
  display: none;
}

hr {
  display: none;
}
</style>
