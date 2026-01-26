import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import router from './router'

import App from './App.vue'

// 入口文件：创建 Vue 应用，并接入 Element Plus 组件库和路由
createApp(App).use(ElementPlus).use(router).mount('#app')


