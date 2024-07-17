// src/plugins/toast.ts
import { App, Plugin } from 'vue'
import { useToast } from 'vue-toastification'

const toastPlugin: Plugin = {
  install (app: App) {
    app.config.globalProperties.$showToast = (message: string, type: 'success' | 'error') => {
      const toast = useToast()
      if (type === 'success') {
        toast.success(message)
      } else if (type === 'error') {
        toast.error(message)
      }
    }
  }
}

export default toastPlugin
