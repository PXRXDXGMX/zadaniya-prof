<template>
  <header>
    <div class="container">
      <nav class="navbar">
        <a href="#" class="logo">
          <i class="fas fa-pen-nib"></i>
          <span>БлогПлатформа</span>
        </a>
        <ul class="nav-links">
          <li><router-link to="/" active-class="active"> <i class="fas fa-home" ></i> Главная</router-link></li>
          <!--          <li><router-link to="/profile" active-class="active"><i class="fas fa-user"></i> Мой профиль</router-link></li>-->
          <li><router-link v-if="token" to="/post" active-class="active"><i class="fas fa-plus-circle"></i> Создать пост</router-link></li>
        </ul>
        <div class="user-actions" >
          <router-link to="/login" v-if="!token" class="btn btn-outline"><i class="fas fa-sign-in-alt"></i> Войти</router-link>
          <router-link to="/register" v-if="!token" class="btn"><i class="fas fa-user-plus"></i> Регистрация</router-link>
          <button v-if="token" class="btn btn-outline" @click="logout">Выйти</button>
        </div>
      </nav>
    </div>
  </header>
</template>

<script setup>
import {computed, ref} from "vue";
import {useRouter, useRoute} from 'vue-router';
import {setToken, store} from "@/auth/auth.js";
import $fetch from "@/fetch/fetch.js";

const router = useRouter();

const token = computed(() => store.value.token)

const logout = async function () {
  await $fetch('/logout', 'get')
  setToken(null)
}
</script>

<style scoped>

</style>