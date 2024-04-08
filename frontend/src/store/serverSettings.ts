// stores/serverSettings.js
import { defineStore } from 'pinia'

export const useServerSettingsStore = defineStore('serverSettings', {
  state: () => ({
    globalTriggeringDisabled: false
  }),
  actions: {
    updateGlobalTriggeringStatus (isDisabled: boolean) {
      this.globalTriggeringDisabled = isDisabled
    }
  }
})
