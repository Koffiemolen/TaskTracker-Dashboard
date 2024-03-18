<template>
  <header>
    <DashboardSearch />
    <div class="user-greeting">
      <h2>Welcome {{ username }}</h2>
      <p>Senior Admin</p>
      <button @click="showSuccessToast">Show Success Toast</button>
      <button @click="showErrorToast">Show Error Toast</button>
      <button @click="toggleGlobalTrigger">Toggle Global Trigger</button>
    </div>
    <div v-if="!globalTrigger" class="global-trigger-warning">
      Global trigger is disabled.
    </div>
  </header>
</template>

<script>
import { defineComponent, ref } from 'vue'
import DashboardSearch from './DashboardSearch.vue'
import { useToast } from 'vue-toastification'

export default defineComponent({
  setup () {
    const toast = useToast()
    const globalTrigger = ref(true) // Initialize the global trigger as true

    const showSuccessToast = () => {
      toast.success('This is a success toast!', {
        // Optional toast options
      })
    }

    const showErrorToast = () => {
      toast.error('This is an error toast!', {
        // Optional toast options
      })
    }

    const toggleGlobalTrigger = () => {
      globalTrigger.value = !globalTrigger.value // Toggle the state
    }

    return { showSuccessToast, showErrorToast, toggleGlobalTrigger, globalTrigger }
  },
  name: 'DashboardHeader',
  components: { DashboardSearch },
  props: {
    username: String
  }
})
</script>

<style scoped>
header {
  display: flex;
  flex-direction: column; /* Adjusted to allow banner to display correctly */
  justify-content: space-between;
  align-items: center;
  padding-bottom: 20px;
  border-bottom: 1px solid #ddd;
  margin-bottom: 20px;
}

.user-greeting {
  text-align: right;
}

.user-greeting h2, .global-trigger-warning {
  margin: 0;
  font-size: 1.5rem;
  color: #333;
}

.global-trigger-warning {
  background-color: #ffdddd;
  color: #d00;
  width: 100%;
  text-align: center;
  padding: 10px 0;
  margin-top: 20px;
}
</style>
