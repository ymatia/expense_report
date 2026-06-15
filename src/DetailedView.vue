<template>
	<div id="DetailedView">
		<EasyDataTable :headers="headers" :items="items" />
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
				headers: [],
				items: []
			}
		},
		created () {
			axios
				.get(generateUrl(`${APP_API_PROXY_URL_PREFIX}/${EX_APP_ID}/data`))
				.then(function (response) {
					console.log(response.data);
					var jsonData = JSON.parse(response.data);
					console.log(jsonData);
					console.log(jsonData["headers"]);
					console.log(jsonData["items"]);
					this.headers = jsonData["headers"];
					this.items = jsonData["items"];
				})
		}
	}
</script>
