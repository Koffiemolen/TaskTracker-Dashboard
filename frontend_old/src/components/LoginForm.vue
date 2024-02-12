<script setup lang="ts">

</script>

<template>
  <div class="login-form">
    <input v-model="username" type="text" placeholder="Username" />
    <input v-model="password" type="password" placeholder="Password" />
    <button @click="login">Login</button>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import AuthService from '../services/AuthService';

export default defineComponent({
  name: 'LoginForm',
  setup() {
    const username = ref('');
    const password = ref('');

    const login = () => {
      AuthService.login({ username: username.value, password: password.value }).then(
          () => {
            // Redirect to dashboard or handle success
          },
          error => {
            // Handle error
          }
      );
    };

    return { username, password, login };
  },
});
</script>


<style scoped>

</style>