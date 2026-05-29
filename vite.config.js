import { createAppConfig } from '@nextcloud/vite-config'
import { defineConfig, splitVendorChunkPlugin } from 'vite'
import { resolve } from 'path'

const yourOverrides = defineConfig({
    plugins: [splitVendorChunkPlugin()],
    build: {
      outDir: 'js',
      emptyOutDir: false,
      rollupOptions: {
        input: resolve(__dirname, 'src/main.ts'),
        output: {
          entryFileNames: 'main.js'
        }
      }
    }
})

export default createAppConfig({
    // entry points
    main: 'src/main.ts'
}, {
    // options
    config: yourOverrides
})