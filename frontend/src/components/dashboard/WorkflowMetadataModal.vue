<!--// src/components/dashboard/WorkflowMetadataModal.vue-->
<!-- components/WorkflowModal.vue -->
<template>
  <div v-if="visible" class="modal">
    <div class="modal-content">
      <span class="close" @click="closeModal">&times;</span>
      <h2>{{ workflowData.WorkflowName }}</h2>
      <p>Status: {{ workflowData.ResultText }}</p>
      <p>Last Run: {{ workflowData.LastLaunchDate }}</p>
      <p>ModifiedOn: {{ workflowData.VersionDate }}</p>
      <p>Enabled: {{ workflowData.Enabled ? 'Yes' : 'No' }}</p>
      <p>Tasks: {{ workflowData.NumberOfTasks }}</p>
      <p>NextLaunch: {{ workflowData.NextLaunchDate }}</p>
      <p>Notes: {{ workflowData.Notes }}</p>
      <p>AgentID: {{ workflowMdata.AgentID }}</p>
      <!-- Loop over workflow metadata items -->
      <div v-for="(item, index) in workflowMdata" :key="index" class="workflow-item">
        <h3><b>{{ item.ConstructTypeName }}</b> : {{ item.ResourceName }}</h3>
        <p>Construct Type: {{ item.ConstructTypeName }}</p>
        <p>Status: {{ item.ResultText }}</p>
        <p>Started On: {{ customFormatDate(item.StartedOn) }}</p>
        <p>Ended On: {{ customFormatDate(item.EndedOn) }}</p>
        <!-- Additional fields as needed -->
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { onMounted, watch, defineComponent, PropType } from 'vue'
import { formatDate } from '@/utils/dateUtils'

export default defineComponent({
  props: {
    visible: Boolean,
    workflowData: Object,
    workflowMdata:
      {
        type: Object as PropType<Array<any>>, // Or use a more specific type
        required: true,
        default: () => ({})
      }
  },
  methods: {
    customFormatDate (value : string) {
      return formatDate(value)
    },
    closeModal () {
      this.$emit('update:visible', false)
    }
  },
  setup (props) {
    onMounted(() => {
      console.log(props.workflowMdata) // Initial log on mount
    })

    watch(() => props.workflowMdata, (newValue) => {
      console.log(newValue) // Log on change
    }, { deep: true })
  }
})
</script>

<style scoped>
.modal {
  display: block;
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgb(0,0,0);
  background-color: rgba(0,0,0,0.4);
}

.modal-content {
  background-color: #fefefe;
  margin: 15% auto;
  padding: 20px;
  border: 1px solid #888;
  width: 80%;
}

.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}

.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}
</style>
