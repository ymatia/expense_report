import { createApp } from 'vue'
import App from './App.vue'

// Vue-Router
import { createMemoryHistory, createRouter } from 'vue-router'
import FinanceOverviewView from './FinanceOverviewView.vue'
import DetailedView from './DetailedView.vue'

const routes = [
  { path: '/financeoverview', component: FinanceOverviewView },
  { path: '/detailed', component: DetailedView },
]

export const router = createRouter({
  history: createMemoryHistory(),
  routes,
})

const app = createApp(App)
app.use(router)
app.mount('#content')
