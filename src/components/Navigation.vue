<template>
	<NcAppNavigation>
		<template #list>
			<NcAppNavigationItem id="app-index"
				:exact="true"
				:name="t('ui_example', 'Home page')"
				:to="{ name: 'ui_example_index' }">
				<template #icon>
					<Home :size="20" />
				</template>
			</NcAppNavigationItem>
			<NcAppNavigationItem id="app-file-picker"
				:name="t('ui_example', 'Files page')"
				:to="{ name: 'ui_example_file_picker' }">
				<template #icon>
					<Folder :size="20" />
				</template>
			</NcAppNavigationItem>
		</template>
	</NcAppNavigation>
</template>

<script>
import NcAppNavigation from '@nextcloud/vue/dist/Components/NcAppNavigation.js'
import NcAppNavigationItem from '@nextcloud/vue/dist/Components/NcAppNavigationItem.js'

import Home from 'vue-material-design-icons/Home.vue'
import Folder from 'vue-material-design-icons/Folder.vue'

export default {
	name: 'Navigation',
	components: {
		NcAppNavigation,
		NcAppNavigationItem,
		Home,
		Folder,
	},
}
</script>
