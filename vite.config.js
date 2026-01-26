import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// Vite + Vue 的最小配置：让 .vue 单文件组件可以被正确编译
export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        secure: false
      }
    }
  }
})


