<template>
	<NcContent app-name="expense-report">
		<NcAppNavigation>
			<NcAppNavigationCaption heading-id="navigation-heading" is-heading name="Reports"/>
			<template #list>
				<NcAppNavigationItem name="Finance Overview">
					<template #icon><svg-icon type="mdi" :path="mdiCheckPath"></svg-icon></template>
				</NcAppNavigationItem>
				<NcAppNavigationItem name="Detailed">
					<template #icon><svg-icon type="mdi" :path="mdiCheckPath"></svg-icon></template>
				</NcAppNavigationItem>
			</template>
		</NcAppNavigation>
		<NcAppContent>
			Select a report from the left
		</NcAppContent>
	</NcContent>
</template>

<script>
    // UI Components
	import { NcContent, NcAppNavigation, NcAppNavigationItem, NcAppContent } from '@nextcloud/vue';
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
		provide() {
			return {
				mdiCheckPath: mdiCheck
			}
		}
	}
</script>
