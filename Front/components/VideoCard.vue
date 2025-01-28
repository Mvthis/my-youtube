<template>
  <nuxt-link :to="'/video/' + video.id" class="video-link">
    <div class="video-card">
      <div class="thumbnail">
        <img
          :src="'http://localhost:5432/' + video.image"
          alt="Video Thumbnail"
        />
        <div class="duration">{{ video.duration }}</div>
      </div>
      <div class="info">
        <h2 class="title">{{ video.name }}</h2>
        <p class="description">{{ video.description }}</p>
        <div class="metadata">
          <div class="creator">{{ video.creator }}</div>
          <div class="views">{{ video.views }} vues</div>
        </div>
      </div>
    </div>
  </nuxt-link>
</template>

<script>
export default {
  props: {
    video: Object,
  },
};
</script>

<style scoped>
.video-card {
  display: flex;
  flex-direction: column;
  overflow: hidden;
  padding: 16px;
  height: 500px;
  width: 500px;
  align-items: flex-start;
}

.thumbnail {
  width: 100%;
  max-width: 900px;
  max-height: 900px;
  margin-bottom: 12px;
  position: relative;
}

.thumbnail img {
  max-width: 900px;
  max-height: 900px;
  width: 100%;
  height: auto;
  border-radius: 25px;
}

.duration {
  position: absolute;
  bottom: 8px;
  right: 8px;
  padding: 4px 8px;
  background-color: rgba(0, 0, 0, 0.6);
  color: #fff;
  border-radius: 4px;
}

.info {
  flex: 1;
}

.title {
  font-size: 1.6rem;
  margin: 0 0 8px;
  color: #ffffff;
}

.description {
  font-size: 14px;
  color: #999393;
  margin: 0 0 12px;
  
}

.metadata {
  flex-direction: column;
  align-items: center;
  font-size: 14px;
  color: #999393;
  justify-content: space-between;
}

.creator {
  margin-right: 8px;
  font-size: 17px;
  margin-top: -8px;
}

.views {
  color: #999393;
  display: none;
}

.video-link {
  text-decoration: none !important;
}
</style>
