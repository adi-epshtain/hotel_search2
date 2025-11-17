<template>
  <div class="hotel-card">
    <img :src="hotel.image" alt="image" class="hotel-img" />

    <div class="details">
      <h3>{{ hotel.name }}</h3>
      <p>{{ hotel.city }}</p>

      <div class="price-box">
        <span class="price">${{ hotel.price }}</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "HotelCard",
  props: {
    hotel: { type: Object, required: true }
  }
};
</script>

<style scoped>
.hotel-card {
  display: flex;
  flex-direction: column;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 10px rgba(0,0,0,0.15);
  margin-bottom: 20px;
  background: #fff;
}
.hotel-img {
  width: 100%;
  height: 180px;
  object-fit: cover;
}
.details {
  padding: 12px;
}
.price-box {
  margin-top: 8px;
  font-size: 18px;
  font-weight: bold;
  color: #0080ff;
}
</style>
