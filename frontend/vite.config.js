import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// 开发态走 Vite 代理，后端即使不开 CORS 也能联调（后端已加 CORS，两者可并存）。
// 生产可设 VITE_API_BASE 指向独立部署的后端。
export default defineConfig({
  plugins: [vue()],
  build: {
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes('node_modules/zrender')) return 'zrender'
          if (id.includes('node_modules/echarts')) return 'echarts'
          if (id.includes('node_modules/vue')) return 'vue'
          if (id.includes('node_modules/lucide-vue-next')) return 'icons'
        }
      }
    }
  },
  server: {
    port: 5173,
    proxy: {
      '/api': { target: 'http://127.0.0.1:8000', changeOrigin: true }
    }
  }
})
