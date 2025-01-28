<template>
  <div id="app" class="mt-5 content">
    <div class="row">
      <input
        type="text"
        v-model="query"
        placeholder="Rechercher"
        class="search"
      />

      <button type="button" class="btn btn-primary" @click="performSearch">
        <img src="../public/search.svg" />
      </button>
    </div>

    <div class="video-card-list">
      <div v-for="video in searchResults" :key="video.objectID">
        <VideoCard
          :video="{
            id: video.id,
            name: video.name,
            image: video.image,
            description: video.description,
            duration: video.duration + ' secondes',
            creator: video.username,
            views: 10,
          }"
        >
        </VideoCard>
      </div>
    </div>

    <div class="none" v-if="searchResults.length === 0">
      <h1>Aucun résultat ... </h1>
    </div>
  </div>
</template>

<script>
import algoliasearch from "algoliasearch/lite";

const searchClient = algoliasearch(
  "8UFMRLN1Q9",
  "3fd23705b13bf89f140ad34776c0eb33"
);
const searchIndex = searchClient.initIndex("myYoutube");

function debounce(func, wait) {
  let timeout;
  return function () {
    const context = this;
    const args = arguments;
    const later = function () {
      timeout = null;
      func.apply(context, args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

export default {
  setup() {
    const query = ref("");
    const searchResults = ref([]);

    const performSearch = debounce(async () => {
      searchResults.value = await searchAlgolia(query.value);
    }, 300);

    async function searchAlgolia(query) {
      try {
        const searchResults = await searchIndex.search(query);
        return searchResults.hits;
      } catch (error) {
        console.error("Error searching Algolia:", error);
        return [];
      }
    }

    onMounted(async () => {
      try {
        performSearch();
      } catch (error) {
        console.error("Error fetching API:", error);
      }
    });

    return {
      query,
      searchResults,
      performSearch,
    };
  },
};
</script>

<style scoped>
row {
  padding-left: 150px;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
}

input {
  width: 30%;
  padding: 10px;
  font-size: 16px;
  border: none;
  border-bottom: 1px solid rgb(14, 211, 27);
  border-radius: 0px;
  box-sizing: border-box;
  background-color: #0f0f0f;
  color: #ffffff;
  margin-left: 35%;
}

input:focus {
  outline: none;
}

button {
  width: auto;
  background-color: rgb(14, 211, 27);
  border: none;
}

button:hover {
  background-color: rgb(181, 15, 232);
}

.video-card-list {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  margin-top: 3rem;
}

hr {
  display: none;
}

img {
  width: 20px;
  height: 20px;
  color: #ffffff;
}

h1 {
  color: #ffffff;
}

.none{
  margin-top: 10rem;
}

</style>
