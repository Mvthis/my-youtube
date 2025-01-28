<template>
  <div class="upload-form">
    <h1>Télécharger une vidéo</h1>
    <form @submit.prevent="upload">
      <div class="form-group">
        <label for="name">Titre:</label>
        <br />
        <br />
        <input type="text" id="name" v-model="name" class="form-control" />
      </div>
      <div class="form-group">
        <label for="description">Description:</label>
        <br />
        <br />
        <input
          type="text"
          id="description"
          v-model="description"
          class="form-control"
        />
      </div>
      <br />
      <br />
      <div class="form-group">
        <label for="video">Vidéo:</label>
        <br />
        <br />
        <input
          type="file"
          id="video"
          ref="videoInput"
          class="form-control-file"
        />
      </div>
      <div class="form-group">
        <label for="image">Image:</label>
        <br />
        <br />
        <input
          type="file"
          id="image"
          ref="imageInput"
          class="form-control-file"
        />
      </div>
      <br />
      <button type="submit" class="btn btn-primary" @click="redirectToDashboard">Télécharger</button>
    </form>
  </div>
</template>

<script>
import { ref } from "vue";
import nuxtStorage from "nuxt-storage";
import apiClient from "~/services/api.js";
import jwt_decode from "jwt-decode";

const token = nuxtStorage.localStorage.getData("token") || "";

const decodedToken = jwt_decode(token);

export default {
  setup() {
    const name = ref("");
    const description = ref("");
    const user_id = decodedToken.id;
    const username = decodedToken.username;
    const token = nuxtStorage.localStorage.getData("token") || "";
    const router = useRouter();
    const videoInput = ref(null);
    const imageInput = ref(null);

    async function upload() {
      try {
        const formData = new FormData();
        formData.append("name", name.value);
        formData.append("description", description.value);
        formData.append("user_id", user_id);
        formData.append("username", username);
        formData.append("source", videoInput.value.files[0]);
        formData.append("image", imageInput.value.files[0]);

        const headers = {
          Authorization: `Bearer ${token}`,
        };

        const response = await apiClient.post(
          "/user/" + user_id + "/video",
          formData,
          {
            headers: headers,
          }
        );

        if (response.data) {
          window.MessageEvent("Vidéo uploadée avec succès");
        } else {
          window.MessageEvent("Erreur lors de l'upload de la vidéo");
        }
      } catch (error) {
        console.error("Error during upload:", error);
      }
    }

    function redirectToDashboard() {
      upload();
      router.push("/dashboard");
    }

    return {
      name,
      description,
      user_id,
      videoInput,
      imageInput,
      upload,
      redirectToDashboard,
    };
  },
};
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
