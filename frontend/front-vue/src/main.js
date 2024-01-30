import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import VueSSE from 'vue-sse'


const app = createApp(App)

app.use(VueSSE)

app.mount('#app')