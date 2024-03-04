<template>
  <div class="card mb-3" style="width: 18rem;">
    <div class="card-body">
      <h5 class="card-title">{{ workflow.WorkflowName }}</h5>
      <h6 class="card-subtitle mb-2 text-muted">Started On: {{ formatDate(workflow.StartedOn) }}</h6>
      <h6 class="card-subtitle mb-2 text-muted">Ended On: {{ formatDate(workflow.EndedOn) }}</h6>
      <p class="card-text">{{ workflow.NumberOfTasks }} tasks
      {{ workflow.ResultText }} </p>
      <div v-if="workflow.ResultCode === 1" class="badge bg-success">Success</div>
      <div v-else-if="workflow.ResultCode === 0" class="badge bg-warning text-dark">Running</div>
      <div v-else class="badge bg-danger">Failed</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'WorkflowCard',
  props: {
    workflow: Object
  },
  methods: {
    formatDate (value) {
      return value ? new Date(value).toLocaleString() : ''
    }
  }
}
</script>

<style scoped>
.card {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 300px;
  text-align: center;
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
</style>
