<template>
  <nav>
    <router-link to="/">Home</router-link> |
    <router-link to="/about">About</router-link> |
    <router-link v-if="!isLoggedIn" to="/login">Login</router-link>
    <button v-if="isLoggedIn" @click="logout">Logout</button>
  </nav>
  <router-view/>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue'
import AuthService from '@/services/AuthService' // Import your AuthService

export default defineComponent({
  name: 'App',
  setup () {
    const isLoggedIn = ref(false)

    // Function to check the user's authentication status
    function checkAuthStatus () {
      const user = AuthService.getCurrentUser()
      isLoggedIn.value = !!user // Sets isLoggedIn to true if user is not null
    }

    // Logout function
    function logout () {
      AuthService.logout() // Your AuthService should handle the logout logic
      isLoggedIn.value = false // Update isLoggedIn state
      // Optionally, redirect the user to the login page or home page after logout
      // router.push('/login'); // Uncomment and import router if you want to redirect
    }

    // Use onMounted lifecycle hook to check auth status when the component mounts
    onMounted(() => {
      checkAuthStatus()
    })

    // Expose the isLoggedIn state and logout function to the template
    return {
      isLoggedIn,
      logout
    }
  }
})
</script>

<!-- Add your styles here -->
<style>
/* Your styles */
</style>
