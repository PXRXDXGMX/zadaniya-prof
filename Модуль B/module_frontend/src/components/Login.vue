<template>
  <div id="login-page" class="page">
    <div class="form-container">
      <h2 class="form-title">С возвращением!</h2>
      <form id="login-form" @submit.prevent="submit">
        <div class="form-group">
          <label for="login-email">Email</label>
          <input type="email" name="email" id="login-email" class="form-control" placeholder="Введите ваш email">
        </div>
        <div class="form-group">
          <label for="login-password">Пароль</label>
          <input name="password" type="password" id="login-password" class="form-control" placeholder="Введите ваш пароль">
        </div>
        <button type="submit" class="btn btn-block"><i class="fas fa-sign-in-alt"></i> Войти</button>
        <div class="text-center mt-3">
          <router-link to="register">Нет аккаунта? Зарегистрируйтесь</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import {onMounted, ref} from "vue";
import $fetch from "@/fetch/fetch";
import {setToken,store} from "@/auth/auth";
import {useRouter} from "vue-router";

const router = useRouter()
async function submit(event) {
  document.querySelectorAll('.error-message').forEach(e => e.remove())

  const response = await $fetch('/login', 'post', new FormData(event.target))
  if (response.error) {
    for (const name in response.data.errors) {
      const input = document.querySelector(`[name="${name}"]`)
      input.setCustomValidity(response.data.errors[name])
      input.insertAdjacentHTML('afterend', `<div class="error-message"><i class="fas fa-exclamation-circle"></i>${response.data.errors[name]}</div>`)
    }
  } else {
    setToken(response.credentials.token)
    console.log(store.value.token)
    router.push('/')
  }
}

onMounted(() => {
  document.querySelectorAll('input').forEach(e => e.onchange = () => e.setCustomValidity(''))
});
</script>

<style scoped>

</style>