<script setup lang="ts">
import NcAppContent from '@nextcloud/vue/components/NcAppContent'
import NcContent from '@nextcloud/vue/components/NcContent'
</script>

<template>
	<NcContent id="exprep" app-name="expense-report">
		<NcAppContent :class="$style.content">
			<div id="exprep">
				<h1>Hello world!</h1>
			</div>
		</NcAppContent>
	</NcContent>
</template>

<style module>
.content {
	display: flex;
	justify-content: center;
	margin: 16px;
}
</style>
