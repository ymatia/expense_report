import { defineConfig } from 'vite'
import { resolve } from 'path'

export default defineConfig({
  build: {
    outDir: 'ex_app/js',          // output into the same folder
    emptyOutDir: false,     // do NOT delete the folder
    sourcemap: false,
    rollupOptions: {
      input: resolve(__dirname, 'src/main.ts'),
      output: {
        entryFileNames: 'main.js',   // overwrite main.js
        format: 'iife'               // classic script, no imports
      }
    }
  }
})