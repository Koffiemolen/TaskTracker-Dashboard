<template>
  <aside class="sidebar">
    <nav>
      <router-link to="/">Dashboard</router-link>
      <router-link to="/errors">Errors</router-link>
      <router-link to="/accounts">Accounts</router-link>
      <router-link to="/workflows">Workflows</router-link>
    </nav>
  </aside>
</template>

<script>
export default {
  name: 'DashboardSidebar'
}
</script>

<style scoped>
.sidebar {
  width: 240px;
  background: #333;
  color: #fff;
  height: 100vh;
  padding: 20px;
}

nav a {
  display: block;
  color: #fff;
  padding: 10px;
  text-decoration: none;
  margin-bottom: 10px;
  background: #444;
  border-radius: 4px;
  transition: background 0.3s ease;
}

nav a:hover {
  background: #555;
}
</style>
