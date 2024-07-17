<!--// src/views/DashboardView.vue-->
<template>
  <div id="dashboard">
    <DashboardSidebar />
    <div class="main-content">
      <DashboardHeader :username="userDetails.name" />
      <section class="workflow-cards-container">
        <WorkflowCard
          v-for="workflow in workflows"
          :key="workflow.resourceId"
          :workflow="workflow"
          @update-enabled="toggleWorkflowEnabled"
          @workflow-started="handleWorkflowStarted"
          @workflow-start-error="handleWorkflowStartError"
          @workflow-click="handleWorkflowSelection"
          @show-toast="showToast"
          @show-modal="handleShowModal"
        />
      </section>
    </div>
  </div>
  <WorkflowMetadataModal
    :workflow="selectedWorkflow"
    v-model:dialog="isModalOpen"
    @update:visible="isModalOpen = $event"
  />
</template>

<script>
import { ref, onMounted } from 'vue'
import APIService from '@/services/APIService'
import DashboardSidebar from '@/components/dashboard/DashboardSidebar.vue'
import DashboardHeader from '@/components/dashboard/DashboardHeader.vue'
import WorkflowCard from '@/components/dashboard/WorkflowCard.vue'
import WorkflowMetadataModal from '@/components/dashboard/WorkflowMetadataModal.vue'

export default {
  name: 'DashboardView',
  components: {
    DashboardSidebar,
    DashboardHeader,
    WorkflowCard,
    WorkflowMetadataModal
  },
  setup () {
    const workflows = ref([])
    const userDetails = ref({ name: 'Loading...' })
    const selectedWorkflow = ref(null)
    const isModalOpen = ref(false)
    const selectWorkflow = (workflow) => {
      selectedWorkflow.value = workflow
      isModalOpen.value = true
    }
    const handleWorkflowSelection = (workflow) => {
      console.log('Opening modal for:', workflow)
      console.log('Previous modal state:', isModalOpen.value)
      selectedWorkflow.value = workflow
      isModalOpen.value = true
      console.log('New modal state:', isModalOpen.value)
    }

    const toggleWorkflowEnabled = (payload) => {
      const workflow = workflows.value.find(w => w.id === payload.id)
      if (workflow) {
        workflow.enabled = payload.enabled
        // Optionally, send an update to the server here if needed.
      }
    }

    const handleWorkflowStarted = ({ workflowId, result }) => {
      console.log(`Workflow ${workflowId} started successfully. Result:`, result)
      // Add any logic to execute when a workflow starts successfully
    }

    const handleWorkflowStartError = ({ workflowId, error }) => {
      console.error(`Error starting workflow ${workflowId}:`, error)
      // Add any logic to execute in case of an error
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
      selectedWorkflow,
      isModalOpen,
      selectWorkflow,
      handleWorkflowStarted,
      handleWorkflowStartError,
      handleWorkflowSelection,
      toggleWorkflowEnabled
    }
  },
  methods: {
    showToast ({ message, type }) {
      if (type === 'success') {
        this.$toast.success(message)
      } else if (type === 'error') {
        this.$toast.error(message)
      }
      // Add more conditions if other toast types
    }

    // handleShowModal (value) {
    //   console.log(`Modal visibility changing to: ${value}`)
    //   this.isModalOpen = value
    // }
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

@media (max-width: 768px) {
  .workflow-cards {
    flex-direction: column;
    align-items: center;
  }
}

</style>
