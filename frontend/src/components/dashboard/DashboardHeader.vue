<template>
  <header>
    <DashboardSearch />
    <div class="user-greeting">
      <h2>Welcome {{ username }}</h2>
      <p>admin</p>
    </div>
    <div v-if="isGlobalTriggeringDisabled" class="red-banner">
      Global Triggering is currently disabled.
    </div>
<!--    <div class="red-banner test-banner">-->
<!--      This is a test banner and should always be visible.-->
<!--    </div>-->
<!--    <button @click="toggleGlobalTriggering">Toggle Global Triggering</button>-->
  </header>
</template>

<script>
import { defineComponent, computed } from 'vue'
import DashboardSearch from './DashboardSearch.vue'
import { useServerSettingsStore } from '@/store/serverSettings'

export default defineComponent({
  name: 'DashboardHeader',
  components: { DashboardSearch },
  props: {
    username: String
  },
  setup () {
    const serverSettingsStore = useServerSettingsStore()
    const isGlobalTriggeringDisabled = computed(() => {
      const result = serverSettingsStore.globalTriggeringDisabled
      console.log('isGlobalTriggeringDisabled', result)
      return result
    })

    function toggleGlobalTriggering () {
      serverSettingsStore.updateGlobalTriggeringStatus(!serverSettingsStore.globalTriggeringDisabled)
    }

    // Now return everything together in a single object
    return {
      isGlobalTriggeringDisabled,
      toggleGlobalTriggering // Include this method for use in the template
    }
  }
})
</script>

<style scoped>
header {
  display: flex;
  flex-direction: column;
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

.red-banner {
  background-color: #ffdddd;
  color: #d00;
  width: 100%;
  text-align: center;
  padding: 10px 0;
  margin-top: 20px;
  transition: opacity 1s ease-in-out;
}
</style>
