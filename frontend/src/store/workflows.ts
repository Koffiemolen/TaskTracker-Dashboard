// store/workflows.ts
import { defineStore } from 'pinia'
import { Workflow } from '@/types/workflow'

export const useWorkflowsStore = defineStore('workflows', {
  state: (): { workflows: Workflow[] } => ({
    workflows: []
  }),
  actions: {
    setWorkflows(workflows: Workflow[]) {
      this.workflows = workflows
    },
    updateWorkflow(updatedWorkflow: Partial<Workflow> & Pick<Workflow, 'ResourceID'>) {
      const index = this.workflows.findIndex(w => w.ResourceID === updatedWorkflow.ResourceID)
      if (index !== -1) {
        // Object.assign(this.workflows[index], updatedWorkflow)
        this.workflows[index] = { ...this.workflows[index], ...updatedWorkflow }
      }
    }
  }
});
