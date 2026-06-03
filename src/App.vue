<template>
	<NcContent app-name="expense-report">
			<NcAppNavigation>
				<NcAppNavigationCaption heading-id="navigation-heading" is-heading name="Reports" />
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
	#content-vue {
		position: relative;
		width: 800px;
		height: 400px;
	}
	
	.styleguide-nc-content {
		position: relative;
		height: 300px;
		background-color: var(--color-background-plain);
		overflow: hidden;
	}

	.navigation__header,
	.navigation__footer {
		display: flex;
		align-items: center;
		gap: 4px;
		padding: 4px;
	}

	.modal-content {
		height: 120px;
		padding: 10px;
	}
</style>