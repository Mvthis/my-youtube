<template>
    <div class="player">
      <div class="video-container">
        <video controls ref="videoPlayer" :src="videoUrl"></video>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      videoUrl: String,
    },
    mounted() {
      this.$refs.videoPlayer.play();
    },
  };
  </script>
  
  <style scoped>
  .player {
    width: 100%;
    max-width: 1200px; 
    margin: 0 auto;
  }
  
  .video-container {
    position: relative;
    padding-bottom: 56.25%;
    height: 0;
    overflow: hidden;
  }
  
  .video-container video {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
  }
  </style>
  