// src/services/APIService.ts
import axios from 'axios'

// Set up the base URL for your API. Ideally, this should be stored in an environment variable or a config file.
const BASE_URL = 'http://127.0.0.1:8000'

// Create an Axios instance for making HTTP requests.
const apiClient = axios.create({
  baseURL: BASE_URL,
  headers: {
    Accept: 'application/json'
  }
})

// Add a request interceptor to inject the Authorization header into every request
// apiClient.interceptors.request.use((config) => {
//   // Attempt to retrieve the user object from local storage
//   const userStr = localStorage.getItem('user')
//   const user = userStr ? JSON.parse(userStr) : null
//
//   // If the user object exists and contains an access token, add the Authorization header
//   if (user && user.accessToken) {
//     config.headers.Authorization = `Bearer ${user.accessToken}`
//   }
//
//   return config
// }, (error) => {
//   // Do something with request error
//   return Promise.reject(error)
// })

apiClient.interceptors.request.use((config) => {
  console.log('Intercepting request:', config)
  const user = JSON.parse(localStorage.getItem('user') || '{}')
  console.log('User:', user)
  console.log('Token', user.access_token)
  if (user && user.access_token) {
    // config.headers.Authorization = `Bearer ${user.accessToken}`
    config.headers.Authorization = `Bearer ${user.access_token}`
    console.log('Added token to headers:', config.headers.Authorization)
  }
  // config.headers.Authorization = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbmlzdHJhdG9yIiwicm9sZXMiOlsiYWRtaW4iXSwiZXhwIjoxNzA5NTgwNjgwfQ.hDVgc3lP9ckPkqm-mL4heQnVYQxA--RyQK4n3GoFHIg'
  return config
}, error => Promise.reject(error))

const dummyUserDetails = {
  name: 'Bertje'
}

export const dummyGlobalTriggering = {
  active: true
}
const APIService = {

  // Function to fetch workflows using the authenticated API call
  async getWorkflows () {
    try {
      const response = await apiClient.get('/workflows/list-all')
      return response.data // Assuming the API response format is directly usable
    } catch (error) {
      console.error('Error fetching workflows:', error)
      // Proper error handling here
      throw error
    }
  },

  // Function to run a workflow using the authenticated API call, input is the workflow ID in
  // url automateapi/workflows/<workflow_id>/run
  async runWorkflow (workflowId: string) {
    try {
      const response = await apiClient.post(`/automateapi/workflows/${workflowId}/run`)
      return response.data // Assuming the API response format is directly usable
    } catch (error) {
      console.error('Error running workflow:', error)
      // Proper error handling here
      throw error
    }
  },

  async getUserDetails () {
    // Simulate an API call with a delay
    await new Promise(resolve => setTimeout(resolve, 500))
    return dummyUserDetails
  }

  // You can add more API call functions here as needed.
  // For example, to fetch user details or to perform other actions that require authentication.

  // async getUserDetails() {...},
  // async createWorkflow(workflowData) {...},
  // etc.
}

export default APIService
