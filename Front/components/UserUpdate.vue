<template>
  <div class="upload-form">
    <h1>Profil</h1>
    <form @submit.prevent="update">
      <div class="form-group">
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="username" class="form-control" />
      </div>
      <div class="form-group">
        <label for="email">Email:</label>
        <input type="text" id="email" v-model="email" class="form-control" />
      </div>
      <div class="form-group">
        <label for="pseudo">Pseudo:</label>
        <input type="text" id="pseudo" v-model="pseudo" class="form-control" />
      </div>
      <div class="form-group">
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" class="form-control" />
      </div>
      <button type="submit" class="btn btn-primary">Update</button>
    </form>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import nuxtStorage from "nuxt-storage";
import apiClient from "~/services/api.js";
import jwt_decode from "jwt-decode";

export default {
  name: "UserUpdate",
  setup() {
    const username = ref("");
    const email = ref("");
    const pseudo = ref("");
    const password = ref("");
    const router = useRouter();

    async function update() {
      try {
        const token = nuxtStorage.localStorage.getData("token") || "";
        const decodedToken = jwt_decode(token);
        const user_id = decodedToken.id;

        const headers = {
          Authorization: `Bearer ${token}`,
        };

        const response = await apiClient.put(
          "/user/" + user_id,
          {
            username: username.value,
            email: email.value,
            pseudo: pseudo.value,
            password: password.value,
          },
          {
            headers: headers,
          }
        );

        if (response.data) {
          router.push("/dashboard");
        } else {
          router.push("/");
        }
      } catch (error) {
        console.error("Error during update:", error);
      }
    }

    onMounted(async () => {
      try {
        const token = nuxtStorage.localStorage.getData("token") || "";
        const decodedToken = jwt_decode(token);
        const user_id = decodedToken.id;

        const headers = {
          Authorization: `Bearer ${token}`,
        };

        const response = await apiClient.get("/user/" + user_id, {
          headers: headers,
        });

        if (response.data) {
          console.log(response.data);
          const userData = response.data["data"];
          username.value = userData[1];
          email.value = userData[2];
          pseudo.value = userData[3];
        }
      } catch (error) {
        console.error("Error fetching user data:", error);
      }
    });

    return {
      username,
      email,
      pseudo,
      password,
      update,
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

.form-control:focus {
  outline: none !important;
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
