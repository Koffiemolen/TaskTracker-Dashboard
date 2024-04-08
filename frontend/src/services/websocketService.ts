// src/services/websocketService.ts
import { useServerSettingsStore } from '@/store/serverSettings'

class WebSocketService {
  private ws: WebSocket | null = null;

  constructor () {
    this.connect()
  }

  connect () {
    this.ws = new WebSocket('ws://localhost:8000/ws')

    this.ws.onmessage = this.onMessage
    this.ws.onclose = this.onClose
    // Handle other events (open, error) as needed
  }

  onMessage (event: MessageEvent) {
    const data = JSON.parse(event.data)
    const serverSettingsStore = useServerSettingsStore()

    // Example handling for server settings change
    if (data.type === 'server_settings_change') {
      const isDisabled = data.data.some((change: any) => change.global_triggering === 0)
      serverSettingsStore.updateGlobalTriggeringStatus(isDisabled)
    }

    // Handle other message types...
  }

  onClose () {
    console.log('WebSocket closed. Attempting to reconnect...')
    setTimeout(() => this.connect(), 5000) // Attempt to reconnect after a delay
  }

  // Add methods for sending messages, handling other events, etc.
}

// Export an instance
export const webSocketService = new WebSocketService()
