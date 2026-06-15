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

	var jsonData = {};
	var str = "";

	export default {
		components: {
			EasyDataTable
		},
		data () {
			return {
				jsonData: { headers: [], data: [] }
			}
		},
		created () {
			axios
				.get(generateUrl(`${APP_API_PROXY_URL_PREFIX}/${EX_APP_ID}/data`))
				.then(function (response) {
					console.log(response.data);
					this.jsonData = JSON.parse(response.data)
				})
		}
	}
</script>
