<template>
  <div class="widget">

    <div class="header">
      <h1 class="welcome-title">Welcome to DesignedVR</h1>
      <p class="welcome-subtitle">Get ready for the experience of a lifetime</p>
    </div>

    <div class="inputs">

      <select v-model="city" class="input-box">
        <option disabled value="">Select city...</option>
        <option v-for="c in cities" :key="getCityValue(c)" :value="getCityValue(c)">
          {{ getCityLabel(c) }}
        </option>
      </select>

      <div class="adults-input-wrapper">
        <label class="adults-label">Adults:</label>
        <div class="adults-controls">
          <button 
            type="button" 
            class="adults-btn" 
            @click="decreaseAdults"
            :disabled="adults <= 1"
          >
            −
          </button>
          <input 
            type="number" 
            v-model.number="adults" 
            class="adults-input"
            :min="1"
            :max="maxAdults"
            @input="validateAdults"
          />
          <button 
            type="button" 
            class="adults-btn" 
            @click="increaseAdults"
            :disabled="adults >= maxAdults"
          >
            +
          </button>
        </div>
      </div>

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
      maxAdults: 20,
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

    increaseAdults() {
      if (this.adults < this.maxAdults) {
        this.adults++;
      }
    },
    
    decreaseAdults() {
      if (this.adults > 1) {
        this.adults--;
      }
    },
    
    validateAdults() {
      if (this.adults < 1) {
        this.adults = 1;
      } else if (this.adults > this.maxAdults) {
        this.adults = this.maxAdults;
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

<style scoped>
.widget {
  max-width: 800px;
  margin: 0 auto;
  padding: 30px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
}

.header {
  text-align: center;
  margin-bottom: 30px;
}

.welcome-title {
  font-size: 2.5em;
  font-weight: 700;
  margin: 0 0 10px 0;
  color: #0080ff;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.welcome-subtitle {
  font-size: 1.2em;
  margin: 0;
  color: #666;
  font-weight: 400;
}

.inputs {
  display: flex;
  gap: 15px;
  align-items: center;
  flex-wrap: wrap;
  margin-bottom: 20px;
}

.input-box {
  padding: 10px 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 16px;
  min-width: 200px;
}

.adults-input-wrapper {
  display: flex;
  align-items: center;
  gap: 10px;
}

.adults-label {
  font-weight: 500;
  white-space: nowrap;
}

.adults-controls {
  display: flex;
  align-items: center;
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
  background: white;
}

.adults-btn {
  background: #f5f5f5;
  border: none;
  padding: 10px 15px;
  font-size: 18px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s;
  min-width: 40px;
}

.adults-btn:hover:not(:disabled) {
  background: #e0e0e0;
}

.adults-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.adults-input {
  border: none;
  padding: 10px;
  width: 60px;
  text-align: center;
  font-size: 16px;
  font-weight: 500;
  outline: none;
}

.adults-input::-webkit-inner-spin-button,
.adults-input::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

.adults-input[type=number] {
  -moz-appearance: textfield;
}

.btn {
  padding: 10px 25px;
  background: #0080ff;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn:hover {
  background: #0066cc;
}

.loading {
  text-align: center;
  padding: 20px;
  font-size: 18px;
}

.results {
  display: grid;
  gap: 20px;
  margin-top: 30px;
}

@media (prefers-color-scheme: dark) {
  .widget {
    background: rgba(26, 26, 26, 0.95);
  }
  
  .welcome-title {
    color: #4da6ff;
  }
  
  .welcome-subtitle {
    color: rgba(255, 255, 255, 0.7);
  }
  
  .input-box,
  .adults-controls,
  .adults-input {
    background: #1a1a1a;
    color: rgba(255, 255, 255, 0.87);
    border-color: #444;
  }
  
  .adults-btn {
    background: #2a2a2a;
    color: rgba(255, 255, 255, 0.87);
  }
  
  .adults-btn:hover:not(:disabled) {
    background: #3a3a3a;
  }
}
</style>
