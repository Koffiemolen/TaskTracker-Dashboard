<!--// src/components/dashboard/WorkflowCard.vue-->
<template>
  <div class="card" :class="{ 'card-enabled': workflow.Enabled, 'card-disabled': !workflow.Enabled, 'is-running': isRunning,
       'is-successful': isSuccessful,
       'has-error': hasError }">
<!--    <button @click="showModal = true">View Details</button>-->
    <button @click="handleWorkflowClick">View Details</button>
    <div class="card-header">
      <h5 class="card-title" :title="workflow.WorkflowName">{{ truncatedWorkflowName }}</h5>
    </div>
    <div class="card-body">
      <div class="workflow-info">
        <div>Started: <time>{{ formatDate(workflow.StartedOn) }}</time></div>
        <div>Ended: <time>{{ formatDate(workflow.EndedOn) }}</time></div>
        <div v-if="workflow.NextLaunchDate">Next Launch: <time>{{ formatDate(workflow.NextLaunchDate) }}</time></div>
      </div>
      <div class="workflow-results">
        <h3 class="workflow-results-header">Workflow Results:</h3>
        <span>{{ workflow.ResultText }}</span>
      </div>
    </div>
    <div class="card-footer">
      <div class="workflow-result">
        <span :class="`result-badge ${getResultClass(workflow.ResultCode)}`">{{ statusInfo.text }}</span>
      </div>
      <div>
        <span class="badge result-badge" :class="`result-${workflow.Result}`.toLowerCase()">{{ workflow.Result }}</span>
      </div>
      <button @click="runWorkflow" :disabled="isButtonDisabled">Run</button>
      <div class="task-count-wrapper">
        <span class="task-count">{{ workflow.NumberOfTasks }} tasks</span>
      </div>
    </div>
    <WorkflowModal
      :visible="showModal"
      :workflowData="workflow"
      :workflowMdata="workflowMetadata"
      @update:visible="showModal = $event"
    />
  </div>
</template>

<script>
import APIService from '@/services/APIService'
import { defineComponent, ref } from 'vue'
import WorkflowModal from '@/components/dashboard/WorkflowMetadataModal.vue'
export default defineComponent({
  name: 'WorkflowCard',
  components: {
    WorkflowModal
  },
  props: {
    workflow: {
      type: Object,
      required: true
    }
  },
  setup (props) {
    const showModal = ref(false)
    // initialize the workflowMetadata ref with an empty array
    const workflowMetadata = ref([])

    const getWorkflowMetaData = async () => {
      try {
        const result = await APIService.getWorkflowMetaData(props.workflow.ResourceID)
        console.log(`Metadata retrieved ${props.workflow.ResourceID} successfully. Result:`, result)
        workflowMetadata.value = result
      } catch (error) {
        console.error(`Error retrieving workflow metadata ${props.workflow.ResourceID}:`, error)
      }
    }

    async function handleWorkflowClick () {
      await getWorkflowMetaData()
      showModal.value = true
    }

    return { showModal, handleWorkflowClick, workflowMetadata }
  },
  data () {
    return {
      isRunning: false,
      isSuccessful: false,
      hasError: false,
      isButtonDisabled: false
    }
  },
  methods: {
    // handleWorkflowClick () {
    //   console.log('Emitting workflow-click with:', this.workflow)
    //   this.$emit('workflow-click', this.workflow)
    // },

    formatDate (value) {
      // Check if the value is falsy or the date is "January 1, 1900 at 12:00:00 AM"
      if (!value) {
        return '-'
      }

      // Check if the date is "January 1, 1900 at 12:00:00 AM"
      const defaultDate = new Date('1900-01-01T00:00:00')
      const date = new Date(value)

      if (date.getTime() === defaultDate.getTime()) {
        return '-'
      }

      const options = {
        hour12: false // Use 24-hour format
      }

      return date.toLocaleString('nl-NL', options)
    },

    getResultClass (resultCode) {
      const statusClassMap = {
        0: 'result-undefined', // Grey
        1: 'result-success', // Green
        2: 'result-failure', // Red
        3: 'result-aborted', // Yellow
        4: 'result-stopped', // Blue
        5: 'result-not-supported', // Grey
        6: 'result-fatal', // Red
        7: 'result-timeout', // Yellow
        8: 'result-halted', // Grey
        9: 'result-paused', // Blue
        10: 'result-unhalted', // Green
        11: 'result-queued', // Dark Grey
        12: 'result-running', // Green
        13: 'result-resuming', // Yellow
        14: 'result-did-not-start', // Grey
        15: 'result-idle', // Light Grey
        16: 'result-initializing', // Blue
        17: 'result-ended', // Grey
        18: 'result-stopping', // Blue
        19: 'result-disconnected' // Dark Red or another indicator color
      }

      return statusClassMap[resultCode] || 'result-unknown' // Default case
    },

    async runWorkflow () {
      this.isButtonDisabled = true

      setTimeout(() => {
        this.isButtonDisabled = false
      }, 5000)

      this.isRunning = true
      try {
        const result = await APIService.runWorkflow(this.workflow.ResourceID)
        this.isRunning = false
        this.isSuccessful = true
        console.log(`Workflow ${this.workflow.ResourceID} started successfully. Result:`, result)
        this.$showToast('Workflow started successfully!', 'success')
      } catch (error) {
        this.isRunning = false
        this.hasError = true
        console.error(`Error starting workflow ${this.workflow.ResourceID}:`, error)
        this.$showToast('Error starting workflow.', 'error')
      }
    },
    async getWorkflowMetaData () {
      try {
        this.isRunning = true
        const result = await APIService.getWorkflowMetaData(this.workflow.ResourceID)
        this.isRunning = false
        this.isSuccessful = true
        console.log(`Metadata retrieved ${this.workflow.ResourceID} successfully. Result:`, result)
      } catch (error) {
        this.isRunning = false
        this.hasError = true
        console.error(`Error retrieving workflow metadata ${this.workflow.ResourceID}:`, error)
      }
    }
  },
  computed: {
    truncatedWorkflowName () {
      const maxLength = 25
      if (this.workflow.WorkflowName.length > maxLength) {
        return `${this.workflow.WorkflowName.substring(0, maxLength)}...`
      }
      return this.workflow.WorkflowName
    },
    statusInfo () {
      const statuses = {
        0: { text: 'Undefined', class: 'bg-secondary' },
        1: { text: 'Success', class: 'bg-success' },
        2: { text: 'Failure', class: 'bg-danger' },
        3: { text: 'Aborted', class: 'bg-warning' },
        4: { text: 'Stopped', class: 'bg-info' },
        5: { text: 'NotSupported', class: 'bg-secondary' },
        6: { text: 'Fatal', class: 'bg-danger' },
        7: { text: 'Timeout', class: 'bg-warning' },
        8: { text: 'Halted', class: 'bg-secondary' },
        9: { text: 'Paused', class: 'bg-info' },
        10: { text: 'Unhalted', class: 'bg-primary' },
        11: { text: 'Queued', class: 'bg-dark' },
        12: { text: 'Running', class: 'bg-primary' },
        13: { text: 'ResumingFromFailure', class: 'bg-warning' },
        14: { text: 'DidNotStart', class: 'bg-secondary' },
        15: { text: 'Idle', class: 'bg-light text-dark' },
        16: { text: 'Initializing', class: 'bg-info' },
        17: { text: 'Ended', class: 'bg-secondary' },
        18: { text: 'Stopping', class: 'bg-info' },
        19: { text: 'AgentDisconnected', class: 'bg-danger' }
      }

      return statuses[this.workflow.ResultCode] || { text: 'Unknown Status', class: 'bg-light text-dark' }
    }
  }
})
</script>

<style scoped>
.card {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow: hidden; /* Ensure children don't overflow rounded corners */
  transition: box-shadow 0.3s;
  width: 300px; /* or 100% for full width on mobile */
}

.card:hover {
  box-shadow: 0 8px 12px rgba(0, 0, 0, 0.2);
}

.card-header {
  background-color: #f4f5f7;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 1rem;
  border-bottom: 1px solid #eaeaea;
  //height: 30px;
}

.card-title {
  font-size: 1.25rem;
  font-weight: bold;
  color: #333;
  margin: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.card-footer {
  display: flex;
  align-items: center; /* This will align flex items vertically in the center */
  justify-content: space-between; /* This spaces out the flex items horizontally */
  padding: 0.5rem 1rem;
}

/* Ensure that the wrappers for the badge and task count do not have any styles
   that would disrupt their alignment, such as different margin or padding values. */
.task-count-wrapper {
  text-align: right;
}

.status-indicators {
  display: flex;
  align-items: center;
}

.status-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 8px;
  font-size: 0.8rem;
  font-weight: bold;
}

.card-enabled {
  border-left: 5px solid #28a745; /* A green border for enabled */
}

.card-disabled {
  background-color: #e9ecef; /* A light grey background for disabled */
  border-left: 5px solid #6c757d; /* A grey border for disabled */
}

.card-body {
  text-align: left; /* Aligns text and inline elements to the right */
}

.workflow-info > div {
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.is-running {
  /* Style for when the workflow is running */
}

.is-successful {
  /* Style for when the workflow completes successfully */
}

.has-error {
  /* Style for when there's an error running the workflow */
}

.result-badge {
  /* Use classes from method getResultClass to set background */
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 8px;
  font-size: 0.8rem;
  margin-bottom: 1rem;
}

.workflow-results-header {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.workflow-results {
  font-size: 0.8rem;
  border-top: 2px solid #ddd; /* Subtle separator */
  padding-top: 1rem; /* Create some space around the results */
}

.card {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 1rem;
  overflow: hidden;
  transition: box-shadow 0.3s ease;
}

.card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.card-header {
  background-color: #f4f5f7;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 1rem;
}

.workflow-title {
  margin: 0;
  font-size: 1.25rem;
}

.result-badge {
  /* Styling based on the result of the last run */
}

.workflow-details {
  padding: 1rem;
  font-size: 0.9rem;
  border-top: 1px solid #eee; /* subtle separator */
}

.card-title {
  margin-bottom: 0.5rem;
  font-size: 1.4rem;
}

.card-subtitle {
  color: #666;
  font-size: 0.95rem;
  margin-bottom: 0.25rem;
}

.card-text {
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

.card h3 {
  color: #333;
  font-size: 1.2rem;
}

.card p {
  color: #666;
  font-size: 0.9rem;
}

.status-icons {
  margin: 10px 0;
}

.switch {
  position: relative;
  display: inline-block;
  width: 60px;
  height: 34px;
  margin-left: 10px; /* Adjust space between badge and switch */
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  -webkit-transition: .4s;
  transition: .4s;
}

.slider:before {
  position: absolute;
  content: "";
  height: 26px;
  width: 26px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  -webkit-transition: .4s;
  transition: .4s;
}

input:checked + .slider {
  background-color: #2196F3;
}

input:focus + .slider {
  box-shadow: 0 0 1px #2196F3;
}

input:checked + .slider:before {
  -webkit-transform: translateX(26px);
  -ms-transform: translateX(26px);
  transform: translateX(26px);
}

.slider.round {
  border-radius: 34px;
}

.slider.round:before {
  border-radius: 50%;
}

.status-indicators {
  display: flex;
  align-items: center;
  justify-content: space-between; /* This will need adjustments based on your layout */
  margin-bottom: 1rem;
}
.result-undefined {
  background-color: #6c757d; /* Bootstrap's secondary color */
  color: white;
}

.result-success {
  background-color: #28a745; /* Bootstrap's success color */
  color: white;
}

.result-failure {
  background-color: #dc3545; /* Bootstrap's danger color */
  color: white;
}

.result-aborted {
  background-color: #ffc107; /* Bootstrap's warning color */
  color: black;
}

.result-stopped {
  background-color: #17a2b8; /* Bootstrap's info color */
  color: white;
}

.result-not-supported {
  background-color: #6c757d; /* Bootstrap's secondary color */
  color: white;
}

.result-fatal {
  background-color: #dc3545; /* Bootstrap's danger color */
  color: white;
}

.result-timeout {
  background-color: #ffc107; /* Bootstrap's warning color */
  color: black;
}

.result-halted {
  background-color: #6c757d; /* Bootstrap's secondary color */
  color: white;
}

.result-paused {
  background-color: #17a2b8; /* Bootstrap's info color */
  color: white;
}

.result-unhalted {
  background-color: #28a745; /* Bootstrap's success color */
  color: white;
}

.result-queued {
  background-color: #343a40; /* Bootstrap's dark color */
  color: white;
}

.result-running {
  background-color: #28a745; /* Bootstrap's success color */
  color: white;
}

.result-resuming {
  background-color: #ffc107; /* Bootstrap's warning color */
  color: black;
}

.result-did-not-start {
  background-color: #6c757d; /* Bootstrap's secondary color */
  color: white;
}

.result-idle {
  background-color: #f8f9fa; /* Bootstrap's light color */
  color: black;
}
</style>
