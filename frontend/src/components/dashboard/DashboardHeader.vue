<template>
  <header>
    <DashboardSearch />
    <div class="user-greeting">
      <h2>Welcome {{ username }}</h2>
<!--      <p>{{ userDetails.role }}</p>-->
      <p>admin</p>
    </div>
    <div v-if="serverSettingsStore.globalTriggeringDisabled" class="red-banner">
      Global Triggering is Disabled.
    </div>
  </header>
</template>

<!--<script setup lang="ts">-->
<script>
import { defineComponent, ref } from 'vue'
import DashboardSearch from './DashboardSearch.vue'
import { useToast } from 'vue-toastification'
import { useServerSettingsStore } from '@/store/serverSettings' // Import the store

export default defineComponent({
  setup () {
    const toast = useToast()
    const serverSettingsStore = useServerSettingsStore() // Use the store

    // Access the globalTrigger directly from the store
    const globalTrigger = serverSettingsStore.globalTriggeringDisabled

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

    // const toggleGlobalTrigger = () => {
    //   globalTrigger.value = !globalTrigger.value // Toggle the state
    // }

    return { showSuccessToast, showErrorToast, serverSettingsStore }
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

@keyframes fadeGlow {
  0%, 100% {
    opacity: 0.5;
    box-shadow: 0 0 5px #ff0000, 0 0 10px #ff0000, 0 0 15px #ff0000, 0 0 20px #ff0000;
  }
  50% {
    opacity: 1;
    box-shadow: 0 0 10px #ff0000, 0 0 20px #ff0000, 0 0 30px #ff0000, 0 0 40px #ff0000, 0 0 50px #ff0000, 0 0 60px #ff0000, 0 0 70px #ff0000;
  }
}

.global-trigger-warning {
  transition: opacity 1s ease-in-out;
  background-color: #ffdddd;
  color: #d00;
  width: 100%;
  text-align: center;
  padding: 10px 0;
  margin-top: 20px;
}
.red-banner {
  background-color: #ffdddd; /* Red background color */
  color: #d00; /* Dark red text color */
  width: 100%;
  text-align: center;
  padding: 10px 0;
  margin-top: 20px;
  transition: opacity 1s ease-in-out;
}

/* You can also include the fadeGlow animation if you want the banner to have a glowing effect */
@keyframes fadeGlow {
  0%, 100% {
    opacity: 0.5;
    box-shadow: 0 0 5px #ff0000, 0 0 10px #ff0000, 0 0 15px #ff0000, 0 0 20px #ff0000;
  }
  50% {
    opacity: 1;
    box-shadow: 0 0 10px #ff0000, 0 0 20px #ff0000, 0 0 30px #ff0000, 0 0 40px #ff0000, 0 0 50px #ff0000, 0 0 60px #ff0000, 0 0 70px #ff0000;
  }
}
</style>
