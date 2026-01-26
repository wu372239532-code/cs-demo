<template>
  <div class="list-container">
    <el-card class="list-card">
      <template #header>
        <div class="card-header">
          <span>风控记录列表</span>
          <el-button type="primary" @click="goToForm">新增记录</el-button>
        </div>
      </template>

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
        <el-table-column prop="punishment" label="处罚内容" min-width="200" show-overflow-tooltip />
        <el-table-column prop="created_at" label="创建时间" width="180" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()

// 加载状态
const loading = ref(false)

// 风控记录列表
const riskList = ref([])

// 获取风控记录列表
const fetchRiskList = async () => {
  loading.value = true

  try {
    // 调用后端接口获取风控记录列表
    const response = await fetch('https://ffdemo.zeabur.app/api/risk')
    const result = await response.json()

    if (result.success) {
      riskList.value = result.data || []
    } else {
      ElMessage.error('获取数据失败')
      riskList.value = []
    }
  } catch (error) {
    console.error('获取数据失败:', error)
    ElMessage.error('获取数据失败，请检查网络连接')
    riskList.value = []
  } finally {
    loading.value = false
  }
}

// 跳转到表单页面
const goToForm = () => {
  router.push('/')
}

// 页面加载时获取数据
onMounted(() => {
  fetchRiskList()
})
</script>

<style scoped>
.list-container {
  padding: 20px;
}

.list-card {
  max-width: 1200px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 18px;
  font-weight: 600;
}
</style>


