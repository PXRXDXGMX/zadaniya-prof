import {createRouter, createWebHistory} from 'vue-router'
export default createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            component: () => import('../components/Home.vue')
        },
        {
            path: '/login',
            component: () => import('../components/Login.vue')
        },
        {
            path: '/register',
            component: () => import('../components/Register.vue')
        },
        {
            path: '/profile',
            component: () => import('../components/Profile.vue')
        },
        {
            path: '/post',
            component: () => import('../components/PostCard.vue')
        },
        {
            path: '/user/:id',
            component: () => import('../components/Profile.vue')
        },
        {
            path: '/edit/:id',
            component: () => import('../components/EditPage.vue'),
            props: true,
        }
        ],
})