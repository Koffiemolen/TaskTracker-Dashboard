// src/services/APIService.ts

// Dummy data simulating API response
const dummyWorkflows = [
  {
    id: 1,
    name: 'PGB-to-CZ',
    lastRun: new Date().toISOString(),
    taskCount: 25,
    status: 'success'
  },
  {
    id: 2,
    name: 'DWH-to-SAS',
    lastRun: new Date().toISOString(),
    taskCount: 15,
    status: 'running'
  },
  {
    id: 3,
    name: 'Incaso-to-‘tHaasje',
    lastRun: new Date().toISOString(),
    taskCount: 2,
    status: 'failed'
  }
]

const dummyUserDetails = {
  name: 'Bertje'
}

const APIService = {
  async getWorkflows () {
    // Simulate an API call with a delay
    await new Promise(resolve => setTimeout(resolve, 500))
    return dummyWorkflows
  },

  async getUserDetails () {
    // Simulate an API call with a delay
    await new Promise(resolve => setTimeout(resolve, 500))
    return dummyUserDetails
  }

  // Add more dummy methods as needed for testing
}

export default APIService
