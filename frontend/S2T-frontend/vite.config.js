import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig(async ({ mode }) => {
  const plugins = [vue()]
  
  if (mode === 'development') {
    try {
      const vueDevTools = await import('vite-plugin-vue-devtools')
      plugins.push(vueDevTools.default())
    } catch (e) {
      // Devtools not available, skip
    }
  }

  return {
    plugins,
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url))
      },
    },
  }
})
