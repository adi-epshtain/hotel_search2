<template>
  <div class="search-widget">

    <div class="inputs">
      <input
        v-model="city"
        placeholder="Search city..."
        class="input"
      />

      <select v-model="adults" class="input">
        <option v-for="n in 10" :value="n">{{ n }} Adults</option>
      </select>

      <button @click="search" class="search-btn">Search</button>
    </div>

    <div v-if="loading" class="loading">Loading…</div>

    <div class="results">
      <HotelCard
        v-for="hotel in results"
        :key="hotel.id"
        :hotel="hotel"
      />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import HotelCard from "./HotelCard.vue";

export default {
  components: { HotelCard },

  data() {
    return {
      city: "",
      adults: 2,
      results: [],
      loading: false
    };
  },

  methods: {
    async search() {
      this.loading = true;

      try {
        const resp = await axios.get("http://127.0.0.1:8000/api/search", {
          params: {
            city: this.city,
            adults: this.adults
          }
        });

        // טיפול בתוצאות לפי המבנה שחוזר מה-BoomNow API
        this.results = resp.data.map(item => ({
          id: item.id,
          name: item.title || item.name,
          city: item.city || "-",
          price: item.price || 0,
          image: item.images?.[0] || "https://via.placeholder.com/400x200"
        }));

      } catch (err) {
        console.error(err);
      }

      this.loading = false;
    }
  }
};
</script>

<style scoped>
.search-widget {
  max-width: 800px;
  margin: 0 auto;
}
.inputs {
  display: flex;
  gap: 8px;
  margin-bottom: 20px;
}
.input {
  padding: 10px;
  flex: 1;
  border-radius: 6px;
  border: 1px solid #ccc;
}
.search-btn {
  padding: 10px 16px;
  background: #007bff;
  color: #fff;
  border-radius: 6px;
  border: none;
}
.results {
  margin-top: 20px;
}
.loading {
  font-size: 18px;
  margin-top: 20px;
}
</style>
