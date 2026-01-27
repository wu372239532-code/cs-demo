<template>
  <div class="list-container">
    <el-card class="list-card">
      <!-- 卡片头部 -->
      <template #header>
        <div class="card-header">
          <span>风控记录列表</span>
          <el-button type="primary" @click="goToForm">
            新增记录
          </el-button>
        </div>
      </template>

      <!-- 表格区域 -->
      <el-table
        v-loading="loading"
        :data="riskList"
        stripe
        style="width: 100%"
        empty-text="暂无数据"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="phone" label="手机号" width="150" />
        <el-table-column prop="name" label="姓名" width="120" />
        <el-table-column
          prop="punishment"
          label="处罚内容"
          min-width="200"
          show-overflow-tooltip
        />
        <el-table-column prop="created_at" label="创建时间" width="180" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
/**
 * ======================
 * 依赖引入
 * ======================
 */
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

/**
 * ======================
 * 路由实例
 * ======================
 */
const router = useRouter()

/**
 * ======================
 * 页面状态数据
 * ======================
 */

// 表格加载状态（控制 loading 动画）
const loading = ref(false)

// 风控列表数据
const riskList = ref([])

/**
 * ======================
 * 接口配置
 * ======================
 * 统一管理接口地址，避免散落在代码中
 */
const API_BASE = 'https://apidemo.zeabur.app'

const API = {
  RISK_LIST: `${API_BASE}/api/risk`
}

/**
 * ======================
 * 获取风控列表数据
 * ======================
 */
const fetchRiskList = async () => {
  loading.value = true

  try {
    // 1. 调用后端接口
    const response = await fetch(API.RISK_LIST)

    // 2. 将接口返回结果转成 JSON
    const result = await response.json()

    // 3. 根据接口返回结构处理数据
    if (result.success) {
      // 成功：赋值给表格数据
      riskList.value = result.data || []
    } else {
      // 接口返回失败状态
      ElMessage.error('获取风控数据失败')
      riskList.value = []
    }
  } catch (error) {
    // 网络异常 / 服务异常
    console.error('获取风控数据异常:', error)
    ElMessage.error('接口请求失败，请检查网络或服务状态')
    riskList.value = []
  } finally {
    // 无论成功还是失败，都关闭 loading
    loading.value = false
  }
}

/**
 * ======================
 * 页面跳转方法
 * ======================
 */
const goToForm = () => {
  // 跳转到表单页面（根据你的路由配置）
  router.push('/')
}

/**
 * ======================
 * 生命周期
 * ======================
 * 页面加载完成后自动请求列表数据
 */
onMounted(() => {
  fetchRiskList()
})
</script>

<style scoped>
/* 页面整体容器 */
.list-container {
  padding: 20px;
}

/* 卡片最大宽度居中 */
.list-card {
  max-width: 1200px;
  margin: 0 auto;
}

/* 卡片头部布局 */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 18px;
  font-weight: 600;
}
</style>
