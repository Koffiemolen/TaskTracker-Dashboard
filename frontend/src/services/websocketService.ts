// src/services/websocketService.ts
import { useServerSettingsStore } from '@/store/serverSettings'

interface WebSocketChannelConfig {
  path: string;
  onMessage: (event: MessageEvent) => void;
}

interface Change {
  RowID: number;
  ID: string;// eslint-disable-next-line
  change_type: string;// eslint-disable-next-line
  global_triggering: number;
  timestamp: string;
}

class WebSocketChannel {
  public config: WebSocketChannelConfig;
  private ws: WebSocket | null = null;

  constructor (config: WebSocketChannelConfig) {
    this.config = config
    this.connect()
  }

  private connect () {
    this.ws = new WebSocket(`ws://localhost:8000${this.config.path}`)

    this.ws.onopen = (event: Event) => {
      console.log(`Connected to ${this.config.path}`)
      // Optionally, invoke onOpen logic here if needed
    }

    this.ws.onmessage = (event: MessageEvent) => {
      this.config.onMessage(event)
    }

    this.ws.onclose = (event: CloseEvent) => {
      console.log(`Disconnected from ${this.config.path}. Attempting to reconnect...`)
      setTimeout(() => this.connect(), 5000)
      // Optionally, invoke onClose logic here if needed
    }

    this.ws.onerror = (event: Event) => {
      console.error(`Error on ${this.config.path}:`, event)
      // Optionally, invoke onError logic here if needed
    }
  }

  // Add methods for sending messages to this channel, etc.
}

interface Subscription {
  messageType: string
  callback: (data: any) => void
}

class WebSocketService {
  private channels: WebSocketChannel[] = []
  private subscriptions: Subscription[] = []

  constructor (channels: WebSocketChannelConfig[]) {
    channels.forEach(channelConfig => this.addChannel(channelConfig))
  }

  addChannel (config: WebSocketChannelConfig) {
    const channel = new WebSocketChannel({
      ...config,
      onMessage: (event: MessageEvent) => {
        const data = JSON.parse(event.data)
        this.notifySubscribers(data)
        if (config.onMessage) config.onMessage(event)
      }
    })
    this.channels.push(channel)
  }

  subscribe (messageType: string, callback: (data: any) => void) {
    this.subscriptions.push({ messageType, callback })
  }

  unsubscribe (messageType: string, callback: (data: any) => void) {
    this.subscriptions = this.subscriptions.filter(sub =>
      !(sub.messageType === messageType && sub.callback === callback))
  }

  private notifySubscribers (data: any) {
    this.subscriptions.forEach(sub => {
      if (data.type === sub.messageType) {
        sub.callback(data)
      }
    })
  }

  // Additional methods...
}

// initialization
const webSocketService = new WebSocketService([
  {
    path: '/ws/globaltriggering',
    onMessage: (event: MessageEvent) => {
      try {
        const message = JSON.parse(event.data)
        console.log('Message from /ws/globaltriggering', event.data)

        if (message.type === 'server_settings_change') {
          const changes = JSON.parse(message.data) as Change[]
          const isDisabled = changes.some(change => {
            console.log('Checking change:', change.global_triggering)
            return change.global_triggering === 0
          })

          console.log('Parsed changes:', changes) // Debugging line to see the parsed changes
          console.log('Global triggering status:', isDisabled ? 'disabled' : 'enabled')

          const serverSettingsStore = useServerSettingsStore()
          serverSettingsStore.updateGlobalTriggeringStatus(isDisabled)
        }
      } catch (error) {
        console.error('Error parsing message:', error)
        console.log('Original message:', event.data)
      }
    }
  },
  {
    path: '/ws/workflow_updates',
    onMessage: (event: MessageEvent) => {
      console.log('Message from /ws/workflow_updates', event.data)
    }
  },
  {
    path: '/ws/workflow_metadata',
    onMessage: (event: MessageEvent) => {
      console.log('Message from /ws/workflow_metadata', event.data)
    }
  }
])

export { webSocketService }
