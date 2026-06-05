<template>
	<NcContent app-name="expense-report" id="content" class="app-expense-report">
		<NcAppNavigation id="app-navigation">
			<NcAppNavigationCaption heading-id="navigation-heading" is-heading name="Reports" id="content"/>
			<template #list>
				<NcAppNavigationItem name="Finance Overview" class="exprep_navigation">
					<template #icon><svg-icon type="mdi" :path="mdiCheckPath"></svg-icon></template>
				</NcAppNavigationItem>
				<NcAppNavigationItem name="Detailed">
					<template #icon><svg-icon type="mdi" :path="mdiCheckPath"></svg-icon></template>
				</NcAppNavigationItem>
			</template>
		</NcAppNavigation>
		<NcAppContent id="app-content">
			<div id="app-navigation-toggle" class="icon-menu"></div>
			Select a report from the left
		</NcAppContent>
	</NcContent>
</template>

<script>
    // UI Components
	import { NcContent, NcAppNavigation, NcAppNavigationItem, NcAppContent } from '@nextcloud/vue'
	// Handling of actions
	import { emit } from '@nextcloud/event-bus'
	// Icons
	import SvgIcon from '@jamescoyle/vue-icon';
	import { mdiCheck } from '@mdi/js';

	export default {
		components: {
			NcContent, 
			NcAppNavigation, 
			NcAppNavigationItem,
			NcAppContent, 
			SvgIcon,
		},
		provide() {
			return {
				mdiCheckPath: mdiCheck,
			}
		},
		data() {
			return {
			}
		},
	}
</script>
