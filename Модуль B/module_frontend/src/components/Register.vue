<template>
  <div id="register-page" class="page">
    <div class="form-container">
      <h2 class="form-title">Присоединяйтесь к нам!</h2>
      <form id="register-form" @submit.prevent="submit">
        <div class="form-group">
          <label for="register-email">Email</label>
          <input name="email" type="email" id="register-email" class="form-control" placeholder="Введите ваш email">
        </div>
        <div class="form-group">
          <label for="register-username">Никнейм</label>
          <input name="nickname" type="text" id="register-username" class="form-control"
                 placeholder="Введите ваш никнейм">
        </div>
        <div class="form-group">
          <label for="register-password">Пароль</label>
          <input name="password" type="password" id="register-password" class="form-control"
                 placeholder="Придумайте надежный пароль">
        </div>
        <button type="submit" class="btn btn-block"><i class="fas fa-user-plus"></i> Зарегистрироваться</button>
        <div class="text-center mt-3">
          <router-link to="/login">Уже есть аккаунт? Войдите</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import {onMounted, ref} from "vue";
import $fetch from "@/fetch/fetch";
import {useRouter} from "vue-router";

const router = useRouter()
const errors = ref(false)

async function submit(event) {
  document.querySelectorAll('.error-message').forEach(e => e.remove())

  const response = await $fetch('/register', 'post', new FormData(event.target))
  if (response.error) {
    for (const name in response.data.errors) {
      const input = document.querySelector(`[name=${name}]`)
      input.setCustomValidity(response.data.errors[name])
      input.insertAdjacentHTML('afterend', `<div class="error-message"><i class="fas fa-exclamation-circle"></i>${response.data.errors[name]}</div>`)
    }
  } else {
    router.push('/login')
  }
}

onMounted(() => {
  document.querySelectorAll('input').forEach(e => e.onchange = () => e.setCustomValidity(''))
});
</script>

<style scoped>

</style>