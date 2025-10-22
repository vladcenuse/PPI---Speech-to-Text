import { createApp } from 'vue'
import App from './App.vue'
import { createAppRouter } from '@/config/app.routes.js'

const app = createApp(App)
const router = createAppRouter()
app.use(router)
app.mount('#app')
