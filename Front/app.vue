<template>
  <Navbar />
  <div id="app" class="mt-5 content">
    <br />
    <br />
    <br />
    <NuxtPage />
  </div>
</template>

<script>
import Navbar from "@/components/Navbar.vue";

export default {
  components: {
    Navbar,
  },
  setup() {
    
    return {};
  },
};
</script>

<style>
@import "bootstrap/dist/css/bootstrap.min.css";

.content {
  position: relative;
}

body {
  background-color: #0f0f0f;
}
</style>
