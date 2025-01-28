<template>
  <div class="comment-list">
    <div v-for="comment in comments.data" :key="comment.id">
      <CommentCard :comment="comment" />
      <hr />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import apiClient from "~/services/api.js";

const comments = ref([]);
const { video_id } = defineProps(["video_id"]);

onMounted(async () => {
  try {
    const response = await apiClient.get(`/video/${video_id}/comments`);
    comments.value = response.data;
  } catch (error) {
    console.error("Error fetching comments:", error);
  }
});
</script>

<style scoped>
.comment-list {
  display: grid;
  grid-template-columns: repeat(1, 1fr);
  gap: 20px;
}

hr {
  display: none;
}
</style>
