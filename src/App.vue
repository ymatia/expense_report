<template>
	<NcContent app-name="expense-report">
		<NcAppNavigation>
			<NcAppNavigationCaption heading-id="navigation-heading" is-heading name="Reports"/>
			<template #list>
				<NcAppNavigationItem name="Finance Overview" @click="loadData('monthly')">
					<template #icon><svg-icon type="mdi" :path="mdiCheckPath"></svg-icon></template>
				</NcAppNavigationItem>
				<NcAppNavigationItem name="Finance by Category" @click="loadData('category')">
					<template #icon><svg-icon type="mdi" :path="mdiCheckPath"></svg-icon></template>
				</NcAppNavigationItem>
				<NcAppNavigationItem name="Cash Flow 00" @click="loadData('cash_flow')">
					<template #icon><svg-icon type="mdi" :path="mdiCheckPath"></svg-icon></template>
				</NcAppNavigationItem>
				<NcAppNavigationItem name="Cash Flow 01" @click="loadData('cash_flow_01')">
					<template #icon><svg-icon type="mdi" :path="mdiCheckPath"></svg-icon></template>
				</NcAppNavigationItem>
				<NcAppNavigationItem name="Finance Overview Previous Year" @click="loadData('monthly_PrevYear')">
					<template #icon><svg-icon type="mdi" :path="mdiCheckPath"></svg-icon></template>
				</NcAppNavigationItem>
				<NcAppNavigationItem name="Debts" @click="loadData('debts')">
					<template #icon><svg-icon type="mdi" :path="mdiCheckPath"></svg-icon></template>
				</NcAppNavigationItem>
				<NcAppNavigationItem name="Debts Summary" @click="loadData('debts_summary')">
					<template #icon><svg-icon type="mdi" :path="mdiCheckPath"></svg-icon></template>
				</NcAppNavigationItem>
				<NcAppNavigationItem name="Reel Usage" @click="loadData('reel_usage')">
					<template #icon><svg-icon type="mdi" :path="mdiCheckPath"></svg-icon></template>
				</NcAppNavigationItem>
			</template>
		</NcAppNavigation>
		<NcAppContent>
			<div id="ReportView" class="main-div">
				<EasyDataTable 
					:headers="headers" 
					:items="items" 
					theme-color="#1d90ff"
					table-class-name="customize-table"
					:loading="loading"
					alternating 
					header-text-direction="center"
    				body-text-direction="left"
				>
					<template #item-Extra="item">
						<div style="text-align: right;">
							{{ item.Extra }}
						</div>
					</template>
				</EasyDataTable>
			</div>
		</NcAppContent>
	</NcContent>
</template>

<script>
    // UI Components
	import { NcContent
		, NcAppNavigation
		, NcAppNavigationItem
		, NcAppContent
		, NcAppNavigationCaption 
		} from '@nextcloud/vue';
	// Handling of actions
	import { emit } from '@nextcloud/event-bus';
	// Icons
	import SvgIcon from '@jamescoyle/vue-icon';
	import { mdiCheck } from '@mdi/js';
	import axios from '@nextcloud/axios';
	import { APP_API_PROXY_URL_PREFIX, EX_APP_ID } from './AppAPI.js';
	import { generateUrl } from '@nextcloud/router';
	import EasyDataTable from "vue3-easy-data-table";
	import "vue3-easy-data-table/dist/style.css";
	import "./MyStyle.css";

	export default {
		components: {
			NcContent, 
			NcAppNavigation, 
			NcAppNavigationItem,
			NcAppContent, 
			SvgIcon,
			EasyDataTable
		},
		data() {
			return {
				mdiCheckPath: mdiCheck,
				headers: [],
				items: [],
				loading: false
			}
		},
		methods: {
			loadData: function(reportName) {
				this.loading = true;
				axios
					.get(generateUrl(`${APP_API_PROXY_URL_PREFIX}/${EX_APP_ID}/data?reportName=${reportName}`))
					.then((response) => {
						var jsonData = JSON.parse(response.data);
						this.headers = jsonData["headers"];
						this.items = jsonData["items"];
						this.loading = false;
				})
			}
		}
	}

</script>
