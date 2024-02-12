<template>
  <div class="login-container">
    <h1>Login</h1>
    <input v-model="username" type="text" placeholder="Username" />
    <input v-model="password" type="password" placeholder="Password" />
    <button @click="handleLogin">Login</button>
    <p v-if="error">{{ error }}</p>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import AuthService from '@/services/AuthService'

export default defineComponent({
  name: 'LoginView',
  setup () {
    const username = ref('')
    const password = ref('')
    const error = ref('')

    const handleLogin = async () => {
      try {
        await AuthService.login(username.value, password.value)
        // Redirect to home page or dashboard here
        error.value = ''
        // Example: router.push('/');
      } catch (e) {
        error.value = 'Failed to login'
        // Handle login error (e.g., show error message)
      }
    }

    return {
      username,
      password,
      error,
      handleLogin
    }
  }
})
</script>

<style scoped>
.login-container {
  /* Style your login container */
}
</style>
