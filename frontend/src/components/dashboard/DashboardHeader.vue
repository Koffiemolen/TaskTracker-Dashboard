<template>
  <header>
    <DashboardSearch />
    <div class="user-greeting">
      <h2>Welcome {{ username }}</h2>
      <p>Senior Admin</p>
    </div>
  </header>
</template>

<script>
import DashboardSearch from './DashboardSearch.vue'

export default {
  name: 'DashboardHeader',
  components: { DashboardSearch },
  props: {
    username: String
  }
}
</script>

<style scoped>
header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 20px;
  border-bottom: 1px solid #ddd;
  margin-bottom: 20px;
}

.user-greeting {
  text-align: right;
}

.user-greeting h2 {
  margin: 0;
  font-size: 1.5rem;
  color: #333;
}
</style>
