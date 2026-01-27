<template>
  <div class="risk-form-container">
    <!-- 天气小部件 -->
    <el-card class="weather-card">
      <div class="weather-widget">
        <el-input
          v-model="weatherCity"
          placeholder="请输入城市名称"
          style="width: 200px; margin-right: 10px"
          clearable
        />
        <el-button
          type="primary"
          @click="handleWeatherQuery"
          :loading="weatherLoading"
        >
          查询天气
        </el-button>
        <div v-if="weatherData" class="weather-result">
          <el-tag type="info" size="large" style="margin-left: 15px">
            {{ weatherData.city }}: {{ weatherData.temperature }}°C
          </el-tag>
          <el-tag type="success" size="large" style="margin-left: 10px">
            {{ weatherData.description }}
          </el-tag>
        </div>
      </div>
    </el-card>

    <el-card class="form-card">
      <template #header>
        <div class="card-header">
          <span>风控处罚表单</span>
        </div>
      </template>

      <el-form
        ref="formRef"
        :model="formData"
        :rules="rules"
        label-width="100px"
        class="risk-form"
      >
        <el-form-item label="手机号" prop="phone">
          <el-input
            v-model="formData.phone"
            placeholder="请输入手机号"
            style="width: 300px"
            clearable
          />
          <el-button
            type="primary"
            @click="handleSearch"
            :loading="searchLoading"
            style="margin-left: 10px"
          >
            查询
          </el-button>
        </el-form-item>

        <el-form-item label="姓名" prop="name">
          <el-input
            v-model="formData.name"
            placeholder="查询后将自动填充"
            style="width: 300px"
            disabled
          />
        </el-form-item>

        <el-form-item label="处罚内容" prop="punishment">
          <el-input
            v-model="formData.punishment"
            type="textarea"
            :rows="4"
            placeholder="请输入处罚内容"
            style="width: 500px"
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="handleSubmit" :loading="submitLoading">
            提交
          </el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()

const formRef = ref(null)

const searchLoading = ref(false)
const submitLoading = ref(false)
const weatherLoading = ref(false)

const weatherCity = ref('')
const weatherData = ref(null)

const formData = reactive({
  phone: '',
  name: '',
  punishment: ''
})

const rules = {
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ],
  punishment: [
    { required: true, message: '请输入处罚内容', trigger: 'blur' }
  ]
}

// ✅ 查询用户信息
const handleSearch = async () => {
  if (!formData.phone) {
    ElMessage.warning('请输入手机号')
    return
  }

  if (!/^1[3-9]\d{9}$/.test(formData.phone)) {
    ElMessage.error('请输入正确的手机号格式')
    return
  }

  searchLoading.value = true

  try {
    const response = await fetch(
      `https://apidemo.zeabur.app/api/user/search?query=${formData.phone}`
    )
    const result = await response.json()

    if (result.success && result.data) {
      formData.name = result.data.name
      ElMessage.success('查询成功')
    } else {
      formData.name = ''
      ElMessage.warning(result.message || '未找到该用户')
    }
  } catch (error) {
    console.error('查询失败:', error)
    ElMessage.error('查询失败，请检查网络连接')
    formData.name = ''
  } finally {
    searchLoading.value = false
  }
}

// ✅ 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) {
      ElMessage.error('请填写完整的表单信息')
      return
    }

    submitLoading.value = true

    try {
      const response = await fetch('https://ff-api.zeabur.app/api/risk', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          phone: formData.phone,
          name: formData.name,
          punishment: formData.punishment
        })
      })

      const result = await response.json()

      if (result.success) {
        ElMessage.success('提交成功')
        router.push('/list')
      } else {
        ElMessage.error(result.error || '提交失败')
      }
    } catch (error) {
      console.error('提交失败:', error)
      ElMessage.error('提交失败，请检查网络连接')
    } finally {
      submitLoading.value = false
    }
  })
}

// ✅ 查询天气
const handleWeatherQuery = async () => {
  if (!weatherCity.value || !weatherCity.value.trim()) {
    ElMessage.warning('请输入城市名称')
    return
  }

  weatherLoading.value = true
  weatherData.value = null

  try {
    const city = encodeURIComponent(weatherCity.value.trim())
    const response = await fetch(
      `https://ff-api.zeabur.app/api/weather?city=${city}`
    )
    const result = await response.json()

    if (result.success && result.data) {
      weatherData.value = result.data
      ElMessage.success('天气查询成功')
    } else {
      ElMessage.error(result.error || '查询天气失败')
      weatherData.value = null
    }
  } catch (error) {
    console.error('查询天气失败:', error)
    ElMessage.error('查询天气失败，请检查网络连接')
    weatherData.value = null
  } finally {
    weatherLoading.value = false
  }
}

// ✅ 重置表单
const handleReset = () => {
  if (formRef.value) {
    formRef.value.resetFields()
  }
  formData.phone = ''
  formData.name = ''
  formData.punishment = ''
}
</script>

<style scoped>
.risk-form-container {
  padding: 20px;
}

.weather-card {
  max-width: 800px;
  margin: 0 auto 20px auto;
}

.weather-widget {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
}

.weather-result {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
}

.form-card {
  max-width: 800px;
  margin: 0 auto;
}

.card-header {
  font-size: 18px;
  font-weight: 600;
}

.risk-form {
  margin-top: 20px;
}
</style>
