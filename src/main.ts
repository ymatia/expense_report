import { createApp } from 'vue'
import App from './App.vue'

// Vue-Router
import { createMemoryHistory, createRouter } from 'vue-router'

import FinanceOverviewView from './FinanceOverviewView.vue'
import DetailedView from './DetailedView.vue'
import ReelUsageView from './ReportView.vue'

import Vue3EasyDataTable from 'vue3-easy-data-table'
import 'vue3-easy-data-table/dist/style.css';

const routes = [
  { path: '/financeoverview', component: FinanceOverviewView },
  { path: '/detailed', component: DetailedView },
  { path: '/report/:reportName', component: ReportView },
]

export const router = createRouter({
  history: createMemoryHistory(),
  routes,
})

const app = createApp(App)
app.use(router)
app.component('EasyDataTable', Vue3EasyDataTable)
app.mount('#content')
