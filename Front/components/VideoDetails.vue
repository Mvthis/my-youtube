<template>
  <div class="name">
    <p v-if="videoData">{{ videoData.name }}</p>
  </div>
  <div class="username">
    <p v-if="videoData">{{ videoData.username }}</p>
  </div>
  <div class="column">
    <div class="col-md-9">
      <div class="description">
        <div class="text">
          <p v-if="videoData">{{ videoData.description }}</p>
        </div>
      </div>
    </div>
    <button
      v-if="videoUsername === username"
      @click="deleteVideo(videoData.id)"
      class="delete-button"
    >
      <img src="../public/trash.svg" />
    </button>
  </div>
</template>

<script>
import apiClient from "~/services/api.js";
import nuxtStorage from "nuxt-storage";
import jwt_decode from "jwt-decode";


export default {
  props: {
    id: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      videoData: null,
      username: "",
      videoUsername: "",
    };
  },

  methods: {
    async deleteVideo(id) {
      try {
        const response = await apiClient.delete(`/video/${id}`);
        this.$router.push("/dashboard");
      } catch (error) {
        console.error("Error during video deletion:", error);
      }
    },
  },

  async mounted() {
    try {
      const response = await apiClient.get("/video/" + this.id);
      this.videoData = response.data.data;

      const token = nuxtStorage.localStorage.getData("token") || "";
      const decodedToken = jwt_decode(token);
      this.username = decodedToken.username;
      this.videoUsername = this.videoData.username;
    } catch (error) {
      console.error("Error fetching video details:", error);
    }
  },
};
</script>

<style scoped>
.name {
  font-size: 2.5rem;
  margin-left: 150px;
  font-weight: bold;
  color: white;
  padding-top: 10px;
}

.username{
  font-size: 1.5rem;
  margin-left: 150px;
  margin-top: -10px;
  margin-bottom: 50px;
  font-weight: bold;
  color: rgb(14, 211, 27);
  padding-top: 10px;
}

.description {
  font-size: 1rem;
  color: white;
  border: 1px solid black;
  background: #272728;
  margin-left: 150px;
  width: 107.3%;
  border-radius: 10px;
}
.text {
  padding: 10px;
}

row {
  display: flex;
  gap: 10px;
}

button {
  background-color: transparent;
  border: none;
  cursor: pointer;
  background-color: rgb(235, 4, 4);
  margin-left: 150px;
  max-width: fit-content;
  border-radius: 5px;
  height: 40px;
  margin-top: 55px;
}

.delete-button img {
  fill: white;
  width: 16px;
  height: 16px;
}
</style>
