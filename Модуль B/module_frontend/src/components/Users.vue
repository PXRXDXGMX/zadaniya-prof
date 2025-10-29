<template>
  <div class="container mt-5">
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h3>Пользователи</h3>
      <button class="btn btn-outline-secondary" @click="logout">Выйти</button>
    </div>
    <p>Здесь будет таблица пользователей.</p>
  </div>
</template>

<script>
import { useAuthStore } from '../auth/auth'
import { useRouter } from 'vue-router'
export default {
  setup() {
    const auth = useAuthStore()
    const router = useRouter()
    function logout() {
      auth.logout()
      router.push('/login')
    }
    return { logout }
  }
}
</script>
