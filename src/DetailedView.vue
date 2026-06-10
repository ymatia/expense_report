<template>
	<div id="DetailedView">
		{{ info }}
	</div>
</template>

<script>
	import axios from '@nextcloud/axios'
	import { APP_API_PROXY_URL_PREFIX, EX_APP_ID } from './AppAPI.js'

	export default {
		data () {
			return {
				info: null
			}
		},
		mounted () {
			axios
				.get(generateUrl(`${APP_API_PROXY_URL_PREFIX}/${EX_APP_ID}/data`))
				.then(response => (this.info = response))
		}
	}
</script>
