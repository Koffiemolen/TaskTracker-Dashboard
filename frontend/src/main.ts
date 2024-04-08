import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css'
import toastPlugin from './plugins/toast'
import { webSocketService } from '@/services/websocketService'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(Toast)
app.use(toastPlugin)

app.provide('webSocketService', webSocketService)

app.mount('#app')
