import { createApp } from 'vue'
import App from './App.vue'

import { setAppName, setAppVersion } from '@nextcloud/vue/dist/initial-state.js'
setAppVersion('33.0.0')
setAppName('expense-report')

const app = createApp(App)
app.mount('#expensereport')
