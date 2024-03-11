<template>
  <div id="dashboard">
    <DashboardSidebar />
    <div class="main-content">
      <DashboardHeader :username="userDetails.name" />
      <section class="workflow-cards-container">
        <WorkflowCard
          v-for="workflow in workflows"
          :key="workflow.id"
          :workflow="workflow"
          @update-enabled="toggleWorkflowEnabled"
        />
      </section>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import APIService from '@/services/APIService'
import DashboardSidebar from '@/components/dashboard/DashboardSidebar.vue'
import DashboardHeader from '@/components/dashboard/DashboardHeader.vue'
import WorkflowCard from '@/components/dashboard/WorkflowCard.vue'

export default {
  name: 'DashboardView',
  components: {
    DashboardSidebar,
    DashboardHeader,
    WorkflowCard
  },
  setup () {
    const workflows = ref([])
    const userDetails = ref({ name: 'Loading...' })
    const toggleWorkflowEnabled = (payload) => {
      const workflow = workflows.value.find(w => w.id === payload.id)
      if (workflow) {
        workflow.Enabled = payload.enabled
        // Optionally, send an update to the server here if needed.
      }
    }

    onMounted(async () => {
      try {
        workflows.value = await APIService.getWorkflows()
        userDetails.value = await APIService.getUserDetails()
      } catch (error) {
        console.error(error.message)
        // Handle error state, e.g., show an error message to the user
      }
    })

    return {
      workflows,
      userDetails,
      toggleWorkflowEnabled
    }
  }
}
</script>

<style>
#dashboard {
  display: flex;
  min-height: 100vh;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.main-content {
  flex: 1;
  padding: 20px;
  background: #f4f5f7;
}

.workflow-cards-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: flex-start; /* align cards to the start of the container */
  padding: 20px;
}

@media (max-width: 768px) {
  .workflow-cards-container {
    justify-content: center; /* center cards on smaller screens */
  }
}

.workflow-cards {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
}

@media (max-width: 768px) {
  .workflow-cards {
    flex-direction: column;
    align-items: center;
  }
}

</style>
