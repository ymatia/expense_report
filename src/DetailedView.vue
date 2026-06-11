<template>
	<div id="DetailedView">
		<VueJsonToHtmlTable :data="jsonData" />
	</div>
</template>

<script>
	import axios from '@nextcloud/axios'
	import { APP_API_PROXY_URL_PREFIX, EX_APP_ID } from './AppAPI.js'
	import { generateUrl } from '@nextcloud/router'
	import VueJsonToHtmlTable from 'vue-json-to-html-table';

	export default {
		components: {
			VueJsonToHtmlTable
		},
		data () {
			return {
				jsonData: null
			}
		},
		mounted () {
			axios
				.get(generateUrl(`${APP_API_PROXY_URL_PREFIX}/${EX_APP_ID}/data`))
				.then(response => (this.jsonData = response))
		}
	}
</script>
