<template>
  <div id="post-form-page" class="page">
    <div class="post-form">
      <h2 class="form-title">Создание публикации</h2>
      <form id="create-post-form" @submit.prevent="submit">
        <div class="form-group">
          <label for="post-title">Заголовок</label>
          <input type="text" name="title" required id="post-title" class="form-control" placeholder="Введите заголовок">
        </div>
        <div class="form-group">
          <label for="post-text">Текст публикации</label>
          <textarea id="post-text" name="description" required class="form-control" rows="5" placeholder="Введите текст публикации"></textarea>
        </div>
        <div class="form-group">
          <label for="post-image">Изображение (опционально)</label>
          <div class="file-upload">
            <input type="file" name="img" id="post-image" accept="image/*">
            <label for="post-image" class="file-upload-label">
              <i class="fas fa-cloud-upload-alt"></i>
              <span>Перетащите изображение сюда или нажмите для выбора</span>
            </label>
          </div>
        </div>
        <div class="form-group text-right">
          <button type="button" class="btn btn-outline"><i class="fas fa-times"></i> Отмена</button>
          <button type="submit" class="btn"><i class="fas fa-paper-plane"></i> Опубликовать</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import $fetch from "@/fetch/fetch.js";
import {onMounted} from "vue";
import {useRouter} from "vue-router";

const router = useRouter();

async function submit () {
  document.querySelectorAll('.error-message').forEach((el) => { el.remove()})

  const response = await $fetch('/posts', 'post', new FormData(event.target))
  console.log(response)
  if (response.error) {
    for (const name in response.data.errors) {
      const input = document.querySelector(`[name="${name}"]`)
      input.setCustomValidity(response.data.errors[name])
      input.insertAdjacentHTML('afterend', `<div class="error-message"><i class="fas fa-exclamation-circle"></i>${response.data.errors[name]}</div>`);
    }
    if (response.status === 403) {
      await router.push('/login')
    }
  }else{

  }
}

onMounted(() => {
  document.querySelectorAll('input').forEach((el) => { el.onchange = () => { el.setCustomValidity('')}})
  document.querySelectorAll('textarea').forEach((el) => { el.onchange = () => { el.setCustomValidity('')}})
})
</script>

<style scoped>

</style>