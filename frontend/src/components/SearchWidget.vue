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

    <div v-if="!loading && results.length > 0" class="results-section">
      <div class="results">
        <HotelCard
          v-for="item in paginatedResults"
          :key="item.id"
          :hotel="item"
        />
      </div>
      
      <div v-if="totalPages > 1" class="pagination">
        <button 
          class="page-btn" 
          @click="goToPage(currentPage - 1)"
          :disabled="currentPage === 1"
        >
          ← Previous
        </button>
        <span class="page-info">
          Page {{ currentPage }} of {{ totalPages }}
        </span>
        <button 
          class="page-btn" 
          @click="goToPage(currentPage + 1)"
          :disabled="currentPage === totalPages"
        >
          Next →
        </button>
      </div>
    </div>

    <div v-if="!loading && results.length === 0 && hasSearched && !searchError" class="no-results">
      No results found. Try a different search.
    </div>
    
    <div v-if="searchError" class="error-message">
      <p><strong>Error:</strong> {{ searchError }}</p>
      <p class="error-hint">Make sure the backend server is running on http://127.0.0.1:8000</p>
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
      cities: [],
      currentPage: 1,
      itemsPerPage: 6,
      hasSearched: false,
      searchError: null
    };
  },
  
  computed: {
    totalPages() {
      return Math.ceil(this.results.length / this.itemsPerPage);
    },
    
    paginatedResults() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.results.slice(start, end);
    }
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
      this.hasSearched = true;
      this.currentPage = 1;
      this.searchError = null;

      try {
        const res = await axios.get("/api/search", {
          params: { city: this.city, adults: this.adults }
        });

        console.log("=== SEARCH RESPONSE ===");
        console.log("Full response:", res);
        console.log("Response data:", res.data);
        console.log("Response data type:", typeof res.data);
        console.log("Is array?", Array.isArray(res.data));
        if (res.data && typeof res.data === 'object') {
          console.log("Response keys:", Object.keys(res.data));
        }
        
        // Handle different response formats
        let data = res.data;
        
        // If it's already an array, use it
        if (Array.isArray(data)) {
          console.log("Data is already an array, length:", data.length);
        } 
        // If it's an object, try to find the array
        else if (data && typeof data === 'object') {
          console.log("Data is an object, searching for array...");
          
          // Try common keys
          const possibleKeys = ['data', 'listings', 'results', 'items', 'hotels', 'properties'];
          let found = false;
          
          for (const key of possibleKeys) {
            if (data[key] && Array.isArray(data[key])) {
              console.log(`Found array in key: ${key}, length: ${data[key].length}`);
              data = data[key];
              found = true;
              break;
            }
          }
          
          // If no common key found, try to find any array value
          if (!found) {
            console.log("No common key found, searching all keys...");
            for (const key in data) {
              if (Array.isArray(data[key])) {
                console.log(`Found array in key: ${key}, length: ${data[key].length}`);
                data = data[key];
                found = true;
                break;
              }
            }
          }
          
          if (!found) {
            console.warn("Could not find array in response, setting empty array");
            console.log("Full data structure:", JSON.stringify(data, null, 2));
            data = [];
          }
        } else {
          console.warn("Unexpected data type:", typeof data);
          data = [];
        }

        console.log("Final data to process:", data);
        console.log("Data length:", data.length);

        if (!Array.isArray(data) || data.length === 0) {
          console.warn("No data to process or data is not an array");
          this.results = [];
          this.loading = false;
          return;
        }

        this.results = data.map((hotel, index) => {
          console.log(`Processing hotel ${index}:`, hotel);
          
          // Handle pictures array - can be pictures or images
          let imageUrl = "https://via.placeholder.com/400x250";
          if (hotel.pictures && Array.isArray(hotel.pictures) && hotel.pictures.length > 0) {
            // Try to get the best quality image
            const firstPic = hotel.pictures[0];
            imageUrl = firstPic.original || firstPic.large || firstPic.regular || firstPic.thumbnail || imageUrl;
            // Fix protocol if missing
            if (imageUrl.startsWith('//')) {
              imageUrl = 'https:' + imageUrl;
            }
          } else if (hotel.images && Array.isArray(hotel.images) && hotel.images.length > 0) {
            imageUrl = hotel.images[0];
          } else if (hotel.image || hotel.photo_url || hotel.thumbnail_url || hotel.main_image) {
            imageUrl = hotel.image || hotel.photo_url || hotel.thumbnail_url || hotel.main_image;
          }
          
          return {
            id: hotel.id || hotel.listing_id || hotel.property_id || `hotel-${index}`,
            name: hotel.title || hotel.name || hotel.listing_title || hotel.property_name || 'Untitled',
            location: hotel.location || hotel.city || hotel.address?.city || hotel.address || this.city,
            city: hotel.city || hotel.address?.city || hotel.address || this.city,
            rating: hotel.rating || hotel.star_rating || hotel.review_score || hotel.reviews?.rating || hotel.review_rating || '4.86',
            guests: hotel.max_guests || hotel.guests || hotel.accommodates || hotel.capacity || hotel.max_capacity,
            bedrooms: hotel.bedrooms || hotel.beds || hotel.bedrooms_count || hotel.room_count || hotel.bedroom_count,
            bathrooms: hotel.bathrooms || hotel.bathrooms_count || hotel.bathrooms_total || hotel.bath_count || hotel.bathroom_count,
            image: imageUrl
          };
        });

        console.log("=== PROCESSED RESULTS ===");
        console.log("Results count:", this.results.length);
        console.log("First result:", this.results[0]);

      } catch (err) {
        console.error("=== SEARCH ERROR ===");
        console.error("Error:", err);
        console.error("Error message:", err.message);
        console.error("Error response:", err.response);
        console.error("Error response data:", err.response?.data);
        console.error("Error response status:", err.response?.status);
        
        // Show user-friendly error message
        if (err.response) {
          // Server responded with error
          console.error(`Server error: ${err.response.status} - ${err.response.statusText}`);
          if (err.response.data) {
            console.error("Error details:", err.response.data);
          }
          this.searchError = `Server error: ${err.response.status} - ${err.response.statusText}`;
        } else if (err.request) {
          // Request was made but no response received
          console.error("No response received from server. Is the backend running?");
          this.searchError = "Cannot connect to server. Please make sure the backend is running on http://127.0.0.1:8000";
        } else {
          // Something else happened
          console.error("Error setting up request:", err.message);
          this.searchError = `Error: ${err.message}`;
        }
        
        this.results = [];
      }

      this.loading = false;
    },
    
    goToPage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    }
  }
};
</script>

<style scoped>
.widget {
  max-width: 1200px;
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

.results-section {
  margin-top: 30px;
}

.results {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 24px;
  margin-bottom: 30px;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin-top: 30px;
  padding: 20px;
}

.page-btn {
  padding: 10px 20px;
  background: #0080ff;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.page-btn:hover:not(:disabled) {
  background: #0066cc;
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  font-size: 14px;
  color: #666;
  font-weight: 500;
}

.no-results {
  text-align: center;
  padding: 40px;
  color: #666;
  font-size: 16px;
  margin-top: 30px;
}

.error-message {
  text-align: center;
  padding: 30px;
  background: #fee;
  border: 2px solid #fcc;
  border-radius: 8px;
  margin-top: 30px;
  color: #c33;
}

.error-message strong {
  display: block;
  margin-bottom: 10px;
  font-size: 18px;
}

.error-hint {
  margin-top: 10px;
  font-size: 14px;
  color: #999;
  font-style: italic;
}

@media (max-width: 768px) {
  .results {
    grid-template-columns: 1fr;
  }
  
  .pagination {
    flex-direction: column;
    gap: 10px;
  }
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
