<template>
	<div id="ReportView" class="main-div">
		<EasyDataTable 
			:headers="headers" 
			:items="items" 
			theme-color="#1d90ff"
    		table-class-name="customize-table"
			:loading="loading"
			alternating 
			body-text-direction="right"
		/>
	</div>
</template>

<script>
	import axios from '@nextcloud/axios';
	import { APP_API_PROXY_URL_PREFIX, EX_APP_ID } from './AppAPI.js';
	import { generateUrl } from '@nextcloud/router';
	import EasyDataTable from "vue3-easy-data-table";
	import "vue3-easy-data-table/dist/style.css";
	import "./MyStyle.css";

	export default {
		components: {
			EasyDataTable
		},
		data: () => ({
			headers: [],
			items: [],
			loading: true
		}),
		methods: {
			loadData: function() {
				axios
					.get(generateUrl(`${APP_API_PROXY_URL_PREFIX}/${EX_APP_ID}/data?reportName=${this.$route.params.reportName}`))
					.then((response) => {
						console.log(response.data);
						var jsonData = JSON.parse(response.data);
						console.log(jsonData);
						console.log(jsonData["headers"]);
						console.log(jsonData["items"]);
						this.headers = jsonData["headers"];
						this.items = jsonData["items"];
						this.loading = false;
				})
			}
		},
		mounted() {
			this.loadData();
		}
	}
</script>


