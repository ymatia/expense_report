import { createApp } from 'vue'
import App from './App.vue'

import { setAppVersion, setAppName } from '@nextcloud/vue/dist/initialState'
setAppVersion('33.0.0')
setAppName('expense-report')

const app = createApp(App)
app.mount('#expensereport')
