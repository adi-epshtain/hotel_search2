<template>
  <div class="widget">
    <input v-model="city" placeholder="City" />
    <select v-model="adults">
      <option v-for="n in 10" :key="n" :value="n">{{ n }} adults</option>
    </select>
    <button @click="search">Search</button>

    <pre v-if="results">{{ results }}</pre>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return { city: "", adults: 2, results: null };
  },
  methods: {
    async search() {
      const resp = await axios.get("/api/search", {
        params: { city: this.city, adults: this.adults }
      });
      this.results = resp.data;
    }
  }
};
</script>
