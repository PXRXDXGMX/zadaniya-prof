<template>
  <div id="home-page" class="page">
    <div class="hero">
      <h1>Поделитесь своими мыслями с миром</h1>
      <p>Присоединяйтесь к сообществу авторов и читателей. Находите вдохновение, делитесь идеями и открывайте новые
        горизонты.</p>
      <router-link to="/post" class="btn btn-secondary"><i class="fas fa-pen-fancy"></i> Начать писать</router-link>
    </div>

    <div class="search-container">
      <i class="fas fa-search search-icon"></i>
      <input type="text" class="search-input" placeholder="Поиск по заголовку..." v-model="search" @input="getPosts">
    </div>

    <div class="posts-grid">
      <!-- Пример публикации 1 -->
      <div v-for="post in data" class="post-card" :key="post.id">
        <img v-if="post.img"
             :src="post.img"
             alt="Изображение публикации" class="post-image">
        <div class="post-content">
          <h3 class="post-title">{{post.title}}</h3>
          <p class="post-text">{{post.description}}</p>
          <div class="post-meta">
            <span class="post-date"><i class="far fa-calendar"></i>{{post.created_at}}</span>
            <span class="post-likes"><i class="fas fa-heart"></i>{{post.count_likes}}</span>
          </div>
          <div class="post-actions">
            <button class="like-btn" :class="post.liked_it ? 'liked' : ''" @click="like(post.id, post.liked_it)">
              <i class="fa-heart" :class="post.liked_it ? 'fas' : 'far' "></i> {{post.liked_it ? 'Убрать лайк' : 'Лайк'}}
            </button>
            <a href="#" class="author-btn">
              <a @click.prevent="router.push(`/user/${post.post_maker_id}`)">Автор</a>
            </a>
          </div>
          <button class="btn btn-outline" @click="goEdit(post)"><i class="fas fa-edit"></i> Редактировать</button>
          <button class="btn btn-danger" @click="deletePost(post.id)"><i class="fas fa-trash"></i> Удалить</button>
        </div>
      </div>
    </div>

    <!-- Пагинация -->
    <ul class="pagination">
      <li><a v-for="i in pages" :class="i === page ? 'active' : ''" @click.prevent="changePage(i)">{{i}}</a></li>
    </ul>
  </div>
</template>

<script setup>
import $fetch from "@/fetch/fetch.js";
import {computed, ref} from "vue";
import {useRouter} from "vue-router";

const data = ref(null)
const search = ref('')
const page = ref(1);
const router = useRouter()

async function getPosts() {
  const response = await $fetch(`/posts`,'get', {search: search.value, page: page.value});
  data.value = response
  console.log(response)
}
function changePage(p) {
  page.value = p
  getPosts()
}
async function like(id, liked_it) {
  if (liked_it) {
    const response = await $fetch(`/posts/${id}/like`, 'delete');
  } else {
    const response = await $fetch(`/posts/${id}/like`, 'post');
  }
  getPosts()
}
async function deletePost(id) {
  await $fetch(`/posts/${id}`, 'delete');
  await getPosts();
}
const pages = computed(function() {
  const min = Math.max(2, page.value - 1);
  const max = Math.max(4, page.value + 1);
  const pages = [1]
  for(let i = min; i <= max; i++) pages.push(i);
  return pages;
})

getPosts()

function goEdit(post)
{
  localStorage.setItem('post', JSON.stringify(post));
  router.push(`/edit/${post.id}`);

}
</script>

<style scoped>
</style>