<template>
	<NcContent app-name="expense-report" id="app-content">
		<NcAppNavigation>
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
		<NcAppContent>
			Select a report from the left
		</NcAppContent>
	</NcContent>
</template>

<script>
    // UI Components
	import NcContent from '@nextcloud/vue/components/NcContent'
	import NcAppNavigation from '@nextcloud/vue/components/NcAppNavigation'
	import NcAppContent from '@nextcloud/vue/components/NcAppContent'
	// Handling of actions
	import { emit } from '@nextcloud/event-bus'
	// Icons
	import SvgIcon from '@jamescoyle/vue-icon';
	import { mdiCheck } from '@mdi/js';

	export default {
		components: {
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

<style lang="scss" scoped>
	#app-content {
		transition: margin-left 100ms ease;
		position: relative;
		overflow-x: hidden;
		align-items: stretch;
	}
</style>