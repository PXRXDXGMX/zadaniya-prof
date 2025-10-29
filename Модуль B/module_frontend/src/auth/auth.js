import {computed, ref} from "vue";

export const store = ref({
    'token': localStorage.getItem('token') !== 'null' && localStorage.getItem('token') ? localStorage.getItem('token') : null
})

export function setToken(newToken) {
    localStorage.setItem('token', newToken)
    store.value.token = newToken
}