<template>
  <div class="hotel-card">
    <img :src="hotel.image" class="hotel-img" />

    <div class="details">
      <h3>{{ hotel.name }}</h3>
      <p class="city">{{ hotel.city }}</p>
      <p class="price">$ {{ hotel.price }}</p>
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
  margin-bottom: 20px;
}

.hotel-img {
  width: 100%;
  height: 180px;
  object-fit: cover;
}

.details {
  padding: 12px;
}

.city {
  font-size: 14px;
  color: #666;
}

.price {
  font-weight: bold;
  color: #0080ff;
  margin-top: 5px;
}
</style>
