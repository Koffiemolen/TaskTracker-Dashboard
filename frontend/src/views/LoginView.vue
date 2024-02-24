// src/components/LoginView.vue
<template>
  <div class="login-container">
    <h1>Login</h1>
    <form @submit.prevent="handleLogin">
      <div>
        <label for="username">Username:</label>
        <input id="username" v-model="username" type="text" required>
      </div>
      <div>
        <label for="password">Password:</label>
        <input id="password" v-model="password" type="password" required>
      </div>
      <div>
        <button type="submit">Login</button>
      </div>
      <p v-if="loginError">{{ loginErrorMessage }}</p>
    </form>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import { useUserStore } from '../store/userStore'
import { useRouter } from 'vue-router'

export default defineComponent({
  setup () {
    const userStore = useUserStore()
    const router = useRouter()
    const username = ref('')
    const password = ref('')
    const loginError = ref(false)
    const loginErrorMessage = ref('')

    const handleLogin = async () => {
      try {
        await userStore.login(username.value, password.value)
        router.push('/')
      } catch (error: unknown) {
        loginError.value = true
        if (error instanceof Error) {
          loginErrorMessage.value = error.message || 'Failed to login'
        } else {
          loginErrorMessage.value = 'Failed to login'
        }
      }
    }

    return {
      username,
      password,
      handleLogin,
      loginError,
      loginErrorMessage
    }
  }
})
</script>

<style scoped>
.login-container {
  max-width: 300px;
  margin: auto;
  padding: 20px;
  text-align: left;
  background: rgba(255, 255, 255, 0.8); /* Slight transparency */
  border-radius: 8px;
}

body {
  display: flex;
  justify-content: center;
  align-items: center;
  background: url('~@/assets/images/loginscreen/LoginIntro.jpg') no-repeat center center fixed;
  background-size: cover;
}

/* Add more styles as needed */
</style>
