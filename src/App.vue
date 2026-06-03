<template>
	<NcContent app-name="expense-report" class="styleguide-nc-content">
		<NcAppNavigation>
			<NcAppNavigationCaption heading-id="navigation-heading" is-heading name="Reports" />
			<template #list>
				<NcAppNavigationItem name="Finance Overview" class="exprep_navigation">
					<template #icon><svg-icon type="mdi" :path="mdiCheckPath"></svg-icon></template>
				</NcAppNavigationItem>
				<NcAppNavigationItem name="Detailed">
					<template #icon><svg-icon type="mdi" :path="mdiCheckPath"></svg-icon></template>
				</NcAppNavigationItem>
			</template>
		</NcAppNavigation>
		<NcAppContent class="exprep_content">
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

<style scoped>
	.styleguide-nc-content {
		background-color: var(--color-background-plain);
		overflow: hidden;
	}
	
	.exprep_navigation {
		width: auto;
		display: block;
	}
	
	.exprep_content {
		width: auto;
		display: block;
	}

</style>