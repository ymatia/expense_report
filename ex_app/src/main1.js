import './bootstrap.js'
import Vue from 'vue'
import App from './App.vue'
import router from './index.js'
import { Tooltip } from '@nextcloud/vue'
import { sync } from 'vuex-router-sync'

Vue.directive('tooltip', Tooltip)
sync(router)

export default new Vue({
	el: '#content',
	router,
	render: h => h(App),
})
