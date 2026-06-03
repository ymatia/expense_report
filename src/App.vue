<template>
	<NcContent app-name="expense-report">
		<div class="styleguide-nc-content">
			<NcAppNavigation>
				<NcAppNavigationCaption heading-id="navigation-heading" is-heading name="Reports" />
				<NcAppNavigationItem name="Finance Overview">
					<template #icon>
						<IconCheck :size="20" />
					</template>
				</NcAppNavigationItem>
				<NcAppNavigationItem name="Detailed">
					<template #icon>
						<IconCheck :size="20" />
					</template>
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
	// import NcAppNavigationToggle from '@nextcloud/vue/components/NcAppNavigationToggle'
	import { NcAppNavigationToggle } from '@nextcloud/vue'
	import { emit } from '@nextcloud/event-bus'
	import IconCheck from 'vue-material-design-icons/Check'

	export default {
		components: {
			IconCheck,
			NcAppNavigationToggle,
		},
		provide() {
			return {
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