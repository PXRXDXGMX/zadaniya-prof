<script setup>
import AppHeader from './components/Header.vue'
import AppFooter from './components/Footer.vue'

</script>

<template>
  <app-header></app-header>

  <!-- Основной контент -->
  <Suspense>
    <main>
      <div class="container">
        <router-view></router-view>
      </div>
    </main>
  </Suspense>


  <app-footer></app-footer>
</template>

<style scoped>
</style>
