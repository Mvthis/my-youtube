<template>
  <div class="video-player">
    <VideoPlayer :videoUrl="videoUrl" />
  </div>
  <div class="button">
    <select
      v-model="selectedFormat"
      @change="updateVideoUrl"
      class="form-select"
    >
      <option v-for="format in formats" :value="format.uri" :key="format.id">
        {{ format.code }}
      </option>
    </select>
    <div v-if="showDropdown" class="dropdown">
      <ul>
        <li v-for="resolution in resolutions" :key="resolution">
          <a @click="selectResolution(resolution)">{{ resolution }}</a>
        </li>
      </ul>
    </div>
  </div>
  <div>
    <VideoDetails :id="videoId" />
  </div>
  <div class="comment-creation">
    <CommentCreation :video_id="videoId" />
  </div>
  <div class="comment-list">
    <CommentList :video_id="videoId" />
  </div>
</template>

<script>
import VideoDetails from "@/components/VideoDetails.vue";
import VideoPlayer from "@/components/VideoPlayer.vue";
import apiClient from "~/services/api.js";

export default {
  components: {
    VideoDetails,
    VideoPlayer,
  },
  data() {
    return {
      videoId: parseInt(this.$route.params.id),
      videoUrl: "",
      formats: [],
      showDropdown: false,
      videos: [],
    };
  },
  async created() {
    try {
      const videoResponse = await apiClient.get(
        "/video/" + this.$route.params.id,
        {
          timeout: 15000,
        }
      );

      this.videoUrl = "http://localhost:5432" + videoResponse.data.data.source;
    } catch (error) {
      console.error("Error fetching video URL:", error);
    }
  },

  async mounted() {
    setTimeout(async () => {
      try {
        const encodedResponse = await apiClient.get(
          "/video/" + this.$route.params.id + "/encoded"
        );
        this.formats = encodedResponse.data.data;
        this.selectedFormat = this.formats[0].uri;
        this.videoUrl = this.selectedFormat;
      } catch (error) {
        console.error("Error fetching encoded formats:", error);
      }
    }, 2000);
  },

  methods: {
    toggleDropdown() {
      this.showDropdown = !this.showDropdown;
    },
    selectResolution(resolution) {
      this.videoUrl = resolution;
    },
    updateVideoUrl() {
      this.videoUrl = this.selectedFormat;
    },
  },
};
</script>

<style scoped>
.video-player {
  margin-top: 16px;
}

.comment-creation {
  margin-top: 100px;
}

.comment-list {
  margin-top: 10px;
}

select {
  margin-top: 5rem;
  margin-left: 150px;
  margin-bottom: 15px;
  max-width: 10rem;
  color: rgb(14, 211, 27);
  font-size: medium;
  padding: 10px;
  background-color: #403e3e;
  border: none;
}
</style>
