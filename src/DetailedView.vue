<template>
	<div id="DetailedView">
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
					.get(generateUrl(`${APP_API_PROXY_URL_PREFIX}/${EX_APP_ID}/data`))
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

<style>
	#DetailedView {
		margin-top: 50px;
	}
	.customize-table {
		--easy-table-border: 1px solid #445269;
		--easy-table-row-border: 1px solid #445269;

		--easy-table-header-font-size: 14px;
		--easy-table-header-height: 50px;
		--easy-table-header-font-color: #c1cad4;
		--easy-table-header-background-color: #2d3a4f;

		--easy-table-header-item-padding: 10px 15px;

		--easy-table-body-even-row-font-color: #fff;
		--easy-table-body-even-row-background-color: #4c5d7a;

		--easy-table-body-row-font-color: #c0c7d2;
		--easy-table-body-row-background-color: #2d3a4f;
		--easy-table-body-row-height: 50px;
		--easy-table-body-row-font-size: 14px;

		--easy-table-body-row-hover-font-color: #2d3a4f;
		--easy-table-body-row-hover-background-color: #eee;

		--easy-table-body-item-padding: 10px 15px;

		--easy-table-footer-background-color: #2d3a4f;
		--easy-table-footer-font-color: #c0c7d2;
		--easy-table-footer-font-size: 14px;
		--easy-table-footer-padding: 0px 10px;
		--easy-table-footer-height: 50px;

		--easy-table-scrollbar-track-color: #2d3a4f;
		--easy-table-scrollbar-color: #2d3a4f;
		--easy-table-scrollbar-thumb-color: #4c5d7a;
		--easy-table-scrollbar-corner-color: #2d3a4f;

		--easy-table-loading-mask-background-color: #2d3a4f;
	}
</style>