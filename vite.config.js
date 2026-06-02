import { createAppConfig } from '@nextcloud/vite-config'
import { defineConfig } from 'vite'
import { resolve } from 'path'

const yourOverrides = defineConfig({
    build: {
      outDir: 'js',
      emptyOutDir: false,
      rollupOptions: {
        input: resolve(__dirname, 'src/main.ts'),
        output: {
          format: 'iife',
		  entryFileNames: 'expense-report-main.js'
        }
      }
    }
})

export default createAppConfig({
    // entry points
    main: 'src/main.ts'
}, {
    // options
    appName: "expense-report",
    config: yourOverrides,
    minify: false,
    OptionalinlineCSS: true
})