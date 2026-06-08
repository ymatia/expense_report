<template>
	<NcContent app-name="expense-report">
		<NcAppNavigation>
			<NcAppNavigationCaption heading-id="navigation-heading" is-heading name="Reports"/>
			<template #list>
				<NcAppNavigationItem name="Finance Overview" to="/financeoverview">
					<template #icon><svg-icon type="mdi" :path="mdiCheckPath"></svg-icon></template>
				</NcAppNavigationItem>
				<NcAppNavigationItem name="Detailed" to="/detailed">
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
