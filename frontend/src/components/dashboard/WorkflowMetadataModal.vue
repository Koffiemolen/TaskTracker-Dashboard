<!--/src/components/dashboard/WorkflowMetadataModal.vue-->
<template>
  <div v-if="visible" class="modal" @click.self="closeModal">
    <div class="modal-content" @click.stop>
      <span class="close" @click="closeModal">&times;</span>
      <h2>{{ workflowData.WorkflowName }}</h2>
      <dl>
        <div><dt>Status:</dt> <dd>{{ workflowData.ResultText }}</dd></div>
        <div><dt>Last Run:</dt> <dd>{{ customFormatDate(workflowData.LastLaunchDate) }}</dd></div>
        <div><dt>Modified On:</dt> <dd>{{ customFormatDate(workflowData.VersionDate) }}</dd></div>
        <div><dt>Enabled:</dt> <dd>{{ workflowData.Enabled ? 'Yes' : 'No' }}</dd></div>
        <div><dt>Tasks:</dt> <dd>{{ workflowData.NumberOfTasks }}</dd></div>
        <div><dt>Next Launch:</dt> <dd>{{ customFormatDate(workflowData.NextLaunchDate) }}</dd></div>
        <div><dt>Notes:</dt> <dd>{{ workflowData.Notes }}</dd></div>
        <div><dt>Agent ID:</dt> <dd>{{ workflowData.AgentID }}</dd></div>
      </dl>
      <section v-for="(item, index) in workflowMdata" :key="index" class="workflow-item">
        <h3>
          {{ item.ConstructTypeName }}: {{ item.ResourceName }}
        </h3>
        <dl>
          <div><dt>Construct Type:</dt> <dd>{{ item.ConstructTypeName }}</dd></div>
          <div><dt>Status:</dt> <dd>{{ item.ResultText }}</dd></div>
          <div><dt>Started On:</dt> <dd>{{ customFormatDate(item.StartedOn) }}</dd></div>
          <div><dt>Ended On:</dt> <dd>{{ customFormatDate(item.EndedOn) }}</dd></div>
        </dl>
      </section>
    </div>
  </div>
</template>

<script lang="ts">
import { onMounted, watch, defineComponent, PropType } from 'vue'
import { formatDate } from '@/utils/dateUtils'

export default defineComponent({
  props: {
    visible: Boolean,
    workflowData: Object as PropType<{ [key: string]: any }>,
    workflowMdata: {
      type: Array as PropType<Array<{ [key: string]: any }>>,
      default: () => []
    }
  },
  methods: {
    customFormatDate (value: string) {
      return formatDate(value)
    },
    closeModal () {
      this.$emit('update:visible', false)
    }
  },
  setup (props) {
    onMounted(() => {
      // Potential Initialization
    })

    watch(() => props.workflowMdata, (newValue) => {
      console.log(newValue)
    }, { deep: true })
  }
})
</script>

<style scoped>
.modal {
  display: flex;
  align-items: center;
  justify-content: center;
  position: fixed;
  z-index: 1000;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0,0,0,0.5);
}

.modal-content {
  background-color: #f4f5f7; /* Matching card header */
  color: #333; /* Text color */
  margin: auto;
  padding: 0.5rem 1rem; /* Padding */
  margin-top: 0; /* Remove default margin */
  border: 1px solid #888;
  width: 90%;
  max-width: 600px;
  border-radius: 5px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.close {
  color: #aaaaaa;
  position: absolute;
  right: 20px;
  top: 15px;
  font-size: 24px;
  font-weight: bold;
}

.close:hover,
.close:focus {
  color: #000;
  text-decoration: none;
  cursor: pointer;
}
h2 {
  background-color: #f3f3f3;
  padding: 10px;
  border-top-left-radius: 5px;
  border-top-right-radius: 5px;
  margin-top: 0;
}

h3 {
  padding-left: 10px;
  border-left: 5px solid #3273dc; /* Use a color that signifies the type of task or trigger */
}

.workflow-item {
  border: 1px solid #ddd;
  margin-top: 15px;
  padding: 10px;
  background-color: #fafafa;
  border-radius: 5px;
}

.status-success {
  color: green;
}

.status-fail {
  color: red;
}

.status-in-progress {
  color: orange;
}
.dt-title {
  font-weight: bold;
  color: #333;
}

dl {
  display: grid;
  grid-template-columns: max-content auto;
  gap: 10px 20px;
  margin: 0;
  padding: 0;
}

dt {
  font-weight: bold;
}

dd {
  margin-left: 15px;
  margin-bottom: 5px;
}
.notes {
  font-style: italic;
  color: #555;
}

.status-badge {
  display: inline-block;
  padding: 5px 10px;
  border-radius: 15px;
  color: #fff;
  background-color: #44c767; /* Change according to status */
  font-size: 0.8em;
}
</style>
