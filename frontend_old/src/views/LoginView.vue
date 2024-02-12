<template>
  <div class="login-container">
    <LoginForm />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import LoginForm from '@/components/LoginForm.vue'; // Ensure the path is correct based on your project structure

export default defineComponent({
  name: 'LoginView',
  components: {
    LoginForm
  }
});
</script>

<style scoped>
.login-container {
  /* Style your login container */
}
</style>
