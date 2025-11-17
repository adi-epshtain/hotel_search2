<template>
  <div class="hotel-card">
    <div class="image-container">
      <img :src="hotel.image" class="hotel-img" :alt="hotel.name" />
    </div>

    <div class="details">
      <h3 class="hotel-title">{{ hotel.name }}</h3>
      <div class="rating">
        <span class="stars">★</span>
        <span class="rating-value">{{ hotel.rating || '4.86' }}</span>
      </div>
      <p class="location">{{ hotel.location || hotel.city }}</p>
      <div class="specs">
        <span>{{ hotel.guests || hotel.maxGuests || '-' }} Guests</span>
        <span>|</span>
        <span>{{ hotel.bedrooms || hotel.beds || '-' }} Bedrooms</span>
        <span>|</span>
        <span>{{ hotel.bathrooms || '-' }} Bathrooms</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "HotelCard",
  props: {
    hotel: Object
  }
};
</script>

<style scoped>
.hotel-card {
  width: 100%;
  border-radius: 12px;
  background: #fff;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
  cursor: pointer;
}

.hotel-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0,0,0,0.2);
}

.image-container {
  width: 100%;
  height: 250px;
  overflow: hidden;
  position: relative;
}

.hotel-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.hotel-card:hover .hotel-img {
  transform: scale(1.05);
}

.details {
  padding: 16px;
}

.hotel-title {
  font-size: 1.1em;
  font-weight: 600;
  margin: 0 0 8px 0;
  color: #333;
  line-height: 1.3;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.rating {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-bottom: 8px;
}

.stars {
  color: #ffa500;
  font-size: 1.1em;
}

.rating-value {
  font-size: 0.95em;
  font-weight: 500;
  color: #333;
}

.location {
  font-size: 0.9em;
  color: #666;
  margin: 0 0 10px 0;
}

.specs {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.85em;
  color: #666;
  flex-wrap: wrap;
}

.specs span {
  white-space: nowrap;
}

@media (prefers-color-scheme: dark) {
  .hotel-card {
    background: #2a2a2a;
  }
  
  .hotel-title {
    color: rgba(255, 255, 255, 0.87);
  }
  
  .rating-value {
    color: rgba(255, 255, 255, 0.87);
  }
  
  .location,
  .specs {
    color: rgba(255, 255, 255, 0.6);
  }
}
</style>
