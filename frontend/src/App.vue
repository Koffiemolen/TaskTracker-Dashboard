// src/App.vue
<template>
  <div id="app">
    <nav>
      <router-link to="/">Home</router-link> |
      <router-link to="/about">About</router-link> |
      <router-link to="/Dashboard">Dashboard</router-link> |
      <router-link v-if="!isLoggedIn" to="/login">Login</router-link>
      <button v-if="isLoggedIn" @click="logout">Logout</button>
    </nav>
    <router-view/>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed } from 'vue'
import { useUserStore } from './store/userStore'
import { useRouter } from 'vue-router'

export default defineComponent({
  setup () {
    const userStore = useUserStore()
    const router = useRouter()

    const isLoggedIn = computed(() => userStore.isLoggedIn)

    const logout = () => {
      userStore.logout()
      router.push('/login') // Redirect the user to the login page
    }

    return {
      isLoggedIn,
      logout
    }
  }
})
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
  margin-right: 10px;
}

nav a.router-link-exact-active {
  color: #42b983;
}

button {
  font-weight: bold;
  cursor: pointer;
}
</style>
