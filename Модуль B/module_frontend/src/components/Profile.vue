<template>
  <section class="profile-page">
    <div class="container">
      <h2>Профиль</h2>
      <div v-if="user">
        <p><strong>Имя:</strong> {{ user.name }}</p>
        <p><strong>Email:</strong> {{ user.email }}</p>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'

const user = ref(null)

onMounted(async () => {
  try {
    const res = await api.get('/user')
    user.value = res.data
  } catch (e) {
    console.error(e)
  }
})
</script>
