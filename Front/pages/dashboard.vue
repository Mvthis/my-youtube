<template>
  <div>
    <h1>Mes vidéos</h1>
  </div>
  <div class="video-list">
    <VideoListByUser/>
  </div>
  <div>
    <button @click="redirectToUpload" class="upload">+</button>
  </div>

</template>
  
<script setup>
  import { useRouter } from 'vue-router';
  import nuxtStorage from 'nuxt-storage';
  const storedUsername = nuxtStorage.localStorage.getData('username') || '';

  const router = useRouter();

  const redirectToUpload = () => {
    router.push('/upload'); 
  };
</script>

<style scoped>
h1 {
  margin: 4rem;
  margin-left: 7rem;
  color: white;
  display: flex;

}
p {
  color: white;
}
.video-list {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
  }

.upload {
  position: fixed;
  bottom: 50px;
  right: 50px;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background-color: #ff0000;
  color: white;
  font-size: 2rem;
  border: none;
  outline: none;
  cursor: pointer;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}

</style>
  