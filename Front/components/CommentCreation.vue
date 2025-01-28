<template>
  <div class="comment-form">
    <textarea
      v-model="commentText"
      placeholder="Ajoutez un commentaire..."
    ></textarea>
    <button @click="postComment">Ajouter un commentaire</button>
  </div>
</template>

<script>
import apiClient from "~/services/api.js";
import nuxtStorage from "nuxt-storage";
import jwt_decode from "jwt-decode";

export default {
  props: {
    video_id: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      commentText: "",
    };
  },
  methods: {
    async postComment() {
      if (!this.commentText || !this.video_id) {
        console.error("Invalid data for posting a comment");
        return;
      }

      try {
        const token = nuxtStorage.localStorage.getData("token") || "";
        if (!token) {
          // Handle the case where the token is not available
          console.error("Token not found");
        }
        const decodedToken = jwt_decode(token);
        const user_id = decodedToken.id;
        const username = decodedToken.username;
        const response = await apiClient.post(
          `/video/${this.video_id}/comment`,
          {
            body: this.commentText,
            user_id,
            video_id: this.video_id,
            username,
          }
        );

        if (response.data) {
          this.commentText = "";
          window.location.reload();
        } else {
          console.error("Invalid response when posting a comment");
        }
      } catch (error) {
        console.error("Error posting comment:", error);
      }
    },
  },
  async asyncData({ app }) {
    const user_id = app.$auth.user.id;
    return { user_id };
  },
};
</script>

<style scoped>
.comment-form {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-left: 150px;
}

textarea {
  width: 88.5%;
  height: 50px;
  border: 1px solid #ccc;
  padding: 10px;
  margin-bottom: 10px;
  background: #0f0f0f;
  color: #fff;
  border-top: none;
  border-right: none;
  border-left: none;
  border: bottom 1px #ffffff;
  resize: none;
}

textarea:focus {
  outline: none;
}

button {
  background: #272727;
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 10px;
  color: #656565;
  cursor: pointer;
  margin-left: 73%;
  font-weight: bold;
}
</style>
