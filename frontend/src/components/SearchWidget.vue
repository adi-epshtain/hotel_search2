<template>
  <div class="widget">

    <div class="inputs">

      <select v-model="city" class="input-box">
        <option disabled value="">Select city...</option>
        <option v-for="c in cities" :key="getCityValue(c)" :value="getCityValue(c)">
          {{ getCityLabel(c) }}
        </option>
      </select>

      <select v-model="adults" class="input-box">
        <option v-for="n in 10" :key="n" :value="n">
          {{ n }} adults
        </option>
      </select>

      <button class="btn" @click="search">Search</button>
    </div>

    <div v-if="loading" class="loading">Loading...</div>

    <div class="results">
      <HotelCard
        v-for="item in results"
        :key="item.id"
        :hotel="item"
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
      loading: false,
      results: [],
      cities: []
    };
  },

  async mounted() {
    await this.loadCities();
  },

  methods: {
    getCityValue(city) {
      if (typeof city === 'string') {
        return city;
      }
      if (city && typeof city === 'object') {
        return city.value || city.name || city.id || String(city);
      }
      return String(city);
    },
    
    getCityLabel(city) {
      if (typeof city === 'string') {
        return city;
      }
      if (city && typeof city === 'object') {
        return city.label || city.name || city.title || city.id || String(city);
      }
      return String(city);
    },
    
    async loadCities() {
      try {
        const res = await axios.get("/api/search/cities");
        console.log("Cities API response:", res.data);
        let data = res.data;
        
        // Handle different response formats
        if (!data) {
          this.cities = [];
          return;
        }
        
        // If it's already an array, use it
        if (Array.isArray(data)) {
          this.cities = data;
          console.log("Cities loaded (array):", this.cities);
          return;
        }
        
        // If it's an object, try to extract the array
        if (data.cities && Array.isArray(data.cities)) {
          this.cities = data.cities;
          console.log("Cities loaded (data.cities):", this.cities);
          return;
        }
        
        if (data.data && Array.isArray(data.data)) {
          this.cities = data.data;
          console.log("Cities loaded (data.data):", this.cities);
          return;
        }
        
        // If we can't find an array, log warning and set empty
        console.warn("Unexpected cities response format:", data);
        this.cities = [];
      } catch (err) {
        console.error("Failed to load cities", err);
        this.cities = [];
      }
    },

    async search() {
      this.loading = true;

      try {
        const res = await axios.get("/api/search", {
          params: { city: this.city, adults: this.adults }
        });

        this.results = res.data.map(hotel => ({
          id: hotel.id,
          name: hotel.title || hotel.name,
          city: this.city,
          price: hotel.price || 100,
          image: hotel.images?.[0] || "https://via.placeholder.com/400x200"
        }));

      } catch (err) {
        console.error(err);
      }

      this.loading = false;
    }
  }
};
</script>
