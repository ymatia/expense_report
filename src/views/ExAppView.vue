<template>
	<NcContent app-name="ui_example">
		<Navigation />
		<NcAppContent>
			<div class="ui-example">
				<h2>{{ t('ui_example', 'ExApp UI example') }}</h2>
				<p>{{ t('ui_example', 'All front-end stuff kept the same for seamless migration for developers. All needed stuff is proxying via AppAPI') }}</p>
				<NcInputField :value="initialState?.initial_value" :label="t('ui_example', 'Initial value')" :disabled="true" />
				<p>
					{{ t('ui_example', 'Initial value from store') }}: {{ initialStateValue }}
				</p>
				<NcButton @click="verifyInitialValue">
					{{ t('ui_example', 'Verify initial value') }}
				</NcButton>

				<div style="margin: 10px 0; display: flex; align-items: center; width: 100%; justify-content: center; flex-direction: column;">
					<NcInputField :value.sync="initialState.initial_sensitive_value"
						:label="t('ui_example', 'Test sensitive value')" />
					<NcButton style="margin: 10px 0;" @click="verifySensitiveValue">
						{{ t('ui_example', 'Verify sensitive value') }}
					</NcButton>
				</div>

				<div style="margin: 10px 0; display: flex; align-items: center; width: 100%; justify-content: center; flex-direction: column;">
					<NcInputField :value.sync="preference_value"
						:label="t('ui_example', 'Test preference sensitive value')" />
					<NcButton style="margin: 10px 0;" @click="verifyPreferenceValue">
						{{ t('ui_example', 'Verify preference value') }}
					</NcButton>
				</div>
			</div>
		</NcAppContent>
	</NcContent>
</template>

<script>
import { loadState } from '@nextcloud/initial-state'
import NcInputField from '@nextcloud/vue/dist/Components/NcInputField.js'
import NcButton from '@nextcloud/vue/dist/Components/NcButton.js'
import NcContent from '@nextcloud/vue/dist/Components/NcContent.js'
import NcAppContent from '@nextcloud/vue/dist/Components/NcAppContent.js'
import Navigation from '../components/Navigation.vue'

export default {
	name: 'ExAppView',
	components: {
		NcContent,
		NcAppContent,
		NcInputField,
		NcButton,
		Navigation,
	},
	data() {
		return {
			initialState: JSON.parse(loadState('app_api', 'ui_example_state')),
			preference_value: 'test_preference_value',
		}
	},
	computed: {
		initialStateValue() {
			return this.$store.getters.getInitialStateValue
		},
	},
	methods: {
		verifyInitialValue() {
			this.$store.dispatch('verifyInitialStateValue', this.initialState?.initial_value)
		},
		verifySensitiveValue() {
			this.$store.dispatch('verifySensitiveValue', this.initialState?.initial_sensitive_value)
		},
		verifyPreferenceValue() {
			this.$store.dispatch('verifyPreferenceValue', this.preference_value)
		},
	},
}
</script>

<style lang="scss" scoped>
.ui-example {
	width: 100%;
	max-width: 600px;
	display: flex;
	flex-direction: column;
	align-items: center;
	margin: 0 auto;
	padding: 30px;

	input, p {
		margin: 20px 0;
	}
}
</style>
