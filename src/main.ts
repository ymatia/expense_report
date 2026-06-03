import { createApp } from 'vue'
import App from './App.vue'

// Create a real DOM mount point for Vue
// const root = document.createElement('div')
// root.id = 'exprep'
// document.body.appendChild(root)

const app = createApp(App)
app.mount('#content')
