<template>
	<NcContent app-name="expense-report">
		<NcAppNavigation>
			<NcAppNavigationCaption heading-id="navigation-heading" is-heading name="Reports"/>
			<template #list>
				<NcAppNavigationItem name="Finance Overview" to="/report/monthly">
					<template #icon><svg-icon type="mdi" :path="mdiCheckPath"></svg-icon></template>
				</NcAppNavigationItem>
				<NcAppNavigationItem name="Finance by Category" to="/report/category">
					<template #icon><svg-icon type="mdi" :path="mdiCheckPath"></svg-icon></template>
				</NcAppNavigationItem>
				<NcAppNavigationItem name="Cash Flow 00" to="/report/cash_flow">
					<template #icon><svg-icon type="mdi" :path="mdiCheckPath"></svg-icon></template>
				</NcAppNavigationItem>
				<NcAppNavigationItem name="Cash Flow 01" to="/report/cash_flow_01">
					<template #icon><svg-icon type="mdi" :path="mdiCheckPath"></svg-icon></template>
				</NcAppNavigationItem>
				<NcAppNavigationItem name="Finance Overview Previous Year" to="/report/monthly_PrevYear">
					<template #icon><svg-icon type="mdi" :path="mdiCheckPath"></svg-icon></template>
				</NcAppNavigationItem>
				<NcAppNavigationItem name="Cash Flow 01" to="/report/debts">
					<template #icon><svg-icon type="mdi" :path="mdiCheckPath"></svg-icon></template>
				</NcAppNavigationItem>
				<NcAppNavigationItem name="Cash Flow 01" to="/report/debts_summary">
					<template #icon><svg-icon type="mdi" :path="mdiCheckPath"></svg-icon></template>
				</NcAppNavigationItem>
				<NcAppNavigationItem name="Reel Usage" to="/report/reel_usage">
					<template #icon><svg-icon type="mdi" :path="mdiCheckPath"></svg-icon></template>
				</NcAppNavigationItem>
			</template>
		</NcAppNavigation>
		<NcAppContent>
			<router-view />
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

	export default {
		components: {
			NcContent, 
			NcAppNavigation, 
			NcAppNavigationItem,
			NcAppContent, 
			SvgIcon
		},
		data() {
			return {
				mdiCheckPath: mdiCheck,
			}
		}
	}

</script>
