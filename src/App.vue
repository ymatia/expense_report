<template>
	<NcContent app-name="expense-report">
		<div class="styleguide-nc-content">
			<NcAppNavigation>
				<NcAppNavigationCaption heading-id="navigation-heading" is-heading name="Reports" />
				<NcAppNavigationItem name="Finance Overview">
					<svg-icon type="mdi" :path="mdiCheckPath"></svg-icon>
				</NcAppNavigationItem>
				<NcAppNavigationItem name="Detailed">
					<svg-icon type="mdi" :path="mdiCheckPath"></svg-icon>
				</NcAppNavigationItem>
			</NcAppNavigation>
		</div>
		<NcAppContent>
			<NcAppNavigationToggle />
			Select a report from the left
		</NcAppContent>
	</NcContent>
</template>

<script>
	import NcContent from '@nextcloud/vue/components/NcContent'
	import NcAppNavigation from '@nextcloud/vue/components/NcAppNavigation'
	import NcAppContent from '@nextcloud/vue/components/NcAppContent'
	import { NcAppNavigationToggle } from '@nextcloud/vue/dist/Components/NcAppNavigationToggle'
	import { emit } from '@nextcloud/event-bus'
	import SvgIcon from '@jamescoyle/vue-icon';
	import { mdiCheck } from '@mdi/js';

	export default {
		components: {
			SvgIcon,
			NcAppNavigationToggle,
		},
		provide() {
			return {
				mdiCheckPath: mdiCheck,
				'NcContent:setHasAppNavigation': () => {},
			}
		},
		data() {
			return {
			}
		},
	}
</script>

<style>
</style>