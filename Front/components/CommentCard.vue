<template>
  <div class="comment-card">
    <div class="comment-user">{{ comment.username }}</div>
    <div class="row">
      <div class="col-md-9">
        <div class="comment-body">{{ comment.body }}</div>
      </div>
      <div class="col-md 10">
        <button
          v-if="comment.username === username"
          @click="deleteComment(comment.id)"
          class="delete-button"
        >
          <img src="../public/trash.svg" />
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import nuxtStorage from "nuxt-storage";
import jwt_decode from "jwt-decode";
import apiClient from "~/services/api.js";

export default {
  props: {
    comment: {
      type: Object,
      required: true,
    },
  },

  data() {
    return {
      username: "",
    };
  },

  methods: {
    async deleteComment(id) {
      try {
        const response = await apiClient.delete(`/comment/${id}`);

        window.location.reload();
      } catch (error) {
        console.error("Error during comment deletion:", error);
      }
    },
  },

  async created() {
    try {
      const token = nuxtStorage.localStorage.getData("token") || "";
      const decodedToken = jwt_decode(token);
      this.username = decodedToken.username;
    } catch (error) {
      console.error("Error during comment creation:", error);
    }
  },
};
</script>

<style scoped>
.comment-card {
  margin-bottom: 10px;
  border: none;
  margin-left: 150px;
  padding: 10px;
  max-width: 500px;
}

.comment-user {
  font-weight: bold;
  color: white;
}

.comment-body {
  margin-top: 5px;
  color: white;
}

.row {
  max-width: 500px;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

button {
  background-color: transparent;
  border: none;
  cursor: pointer;
  background-color: rgb(235, 4, 4);
  max-width: fit-content;
  border-radius: 5px;
}

.delete-button img {
  fill: white; /* Set the fill color of the SVG to white */
  width: 16px; /* Adjust the width as needed */
  height: 16px; /* Adjust the height as needed */
}
</style>
