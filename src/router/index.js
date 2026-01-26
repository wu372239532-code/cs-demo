import { createRouter, createWebHistory } from 'vue-router'
import RiskForm from '../components/RiskForm.vue'
import List from '../components/List.vue'

// 创建路由配置
const routes = [
  {
    path: '/',
    name: 'RiskForm',
    component: RiskForm
  },
  {
    path: '/list',
    name: 'List',
    component: List
  }
]

// 创建路由实例
const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router

