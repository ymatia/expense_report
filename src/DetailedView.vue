<template>
	<div id="DetailedView">
		<EasyDataTable :headers="jsonData.headers" :items="jsonData.data" />
	</div>
</template>

<script>
	import axios from '@nextcloud/axios';
	import { APP_API_PROXY_URL_PREFIX, EX_APP_ID } from './AppAPI.js';
	import { generateUrl } from '@nextcloud/router';
	import EasyDataTable from "vue3-easy-data-table";
	import "vue3-easy-data-table/dist/style.css";

	export default {
		components: {
			EasyDataTable
		},
		data () {
			return {
				jsonData: {}
			}
		},
		created () {
			axios
				.get(generateUrl(`${APP_API_PROXY_URL_PREFIX}/${EX_APP_ID}/data`))
				.then(response => (this.jsonData = response))
		}
	}
</script>
