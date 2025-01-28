<template>
    <div class="upload-form">
    <h1>S'inscrire</h1>
    <form @submit.prevent="register">
      <div class="form-group">
        <label for="username">Username:</label>
        <br/>
        <br/>
        <input type="text" id="username" v-model="username" class="form-control"/>
      </div>
      <br/>
      <br/>
      <div class="form-group">
        <label for="email">Email:</label>
        <br/>
        <br/>
        <input type="text" id="email" v-model="email" class="form-control"/>
      </div>
      <br/>
      <br/>
      <div class="form-group">
        <label for="pseudo">Pseudo:</label>
        <br/>
        <br/>
        <input type="text" id="pseudo" v-model="pseudo" class="form-control" />
      </div>
      <br/>
      <br/>
      <div class="form-group">
        <label for="password">Mot de passe:</label>
        <br/>
        <br/>
        <input type="password" id="password" v-model="password" class="form-control"/>
      </div>
      <br/>
      <br/>
      <button type="submit" class="btn btn-primary">S'inscrire</button>
    </form>
  </div>
</template>

<script setup>
  import nuxtStorage from 'nuxt-storage';
  import { ref } from 'vue';
  import apiClient from '~/services/api.js';

  const username = ref('');
  const email = ref('');
  const pseudo = ref('');
  const password = ref('');
  const router = useRouter();

  async function register() {
    try {
      const response = await apiClient.post('/user', {
        username: username.value,
        email: email.value,
        pseudo: pseudo.value,
        password: password.value,
      });

      if (response.data) {

        nuxtStorage.localStorage.setData('username', username.value);
        router.push('/login');
        } else {
            router.push('/');
        }
    } catch (error) {
      console.error('Error during login:', error);
    }
  }
</script>

<style scoped>
.upload-form {
  max-width: 700px;
  margin:  auto;
  margin-top: 50px;
  padding:20px;
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
  border-bottom: bottom 1px #53c836;
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
  background-color:rgb(14, 211, 27);
  color: #fff;
  padding: 10px 20px;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}

.btn-primary:hover {
  background-color:rgb(10, 83, 15);
}

h1 {
  color: #fff;
  padding: 30px;
}
</style>